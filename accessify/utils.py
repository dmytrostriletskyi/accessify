"""
Provide utils.
"""
import inspect

COMMERCIAL_AT_SYMBOL = '@'
DISABLE_ACCESSIFY_ENV_VARIABLE_NAME = 'DISABLE_ACCESSIFY'
MARK_MEMBER_RAISES_EXCEPTION = 'raise {exception_name}'


class AccessModifierTypes:
    """
    Provide access modifier types.
    """

    PUBLIC = 'public'
    PRIVATE = 'private'
    PROTECTED = 'protected'


ACCESS_WRAPPERS_NAMES = (
    AccessModifierTypes.PRIVATE + '_wrapper',
    AccessModifierTypes.PROTECTED + '_wrapper',
)


class ClassMemberMagicMethodNames:
    """
    Provide class members magic method names.
    """

    NAME = '__name__'
    SELF = '__self__'
    THROWS = '__throws__'


class ClassMemberTypes:
    """
    Provide class members types.
    """

    GETTER = 'getter'
    SETTER = 'setter'
    DELETER = 'deleter'
    METHOD = 'method'
    STATIC_METHOD = 'staticmethod'
    CLASS_METHOD = 'classmethod'


def does_classes_contain_private_method(classes, method):
    """
    Check if at least one of provided classes contains a method.

    If one of the classes contains the method and this method has private access level, return true and class
    that contains the method.
    """
    for class_ in classes:
        if hasattr(class_, method.__name__):
            if getattr(class_, method.__name__).__name__ in 'private_wrapper':
                return True, class_

    return False, None


def find_decorated_method(function):
    """
    Get bottom function under specified decorator in recursive mode.

        @private
        @staticmethod
        @decorator
        def function():
            pass

    When you pass `class.function` objects, you do not pass `class.function` actually. You pass a reference to
    private object (e.g. `function private.<locals>.private_wrapper at 0x1065cf2f0`).
    """
    if isinstance(function, property):
        return function

    if function.__class__.__name__ in (ClassMemberTypes.STATIC_METHOD, ClassMemberTypes.CLASS_METHOD):
        return find_decorated_method(function.__func__)

    if function.__closure__ is not None:
        return find_decorated_method(function.__closure__[0].cell_contents)

    return function


def isprop(object_):
    """
    Return true if the object is a property of the class.

    Used to extent inspect built-in Python module.

    References:
        - https://docs.python.org/3/library/inspect.html.
    """
    return isinstance(object_, property)


class ClassMember:
    """
    Provide implementation of class member.
    """

    def __init__(self, name, object_, class_, type_=None):
        """
        Constructor.

        `self.method` is a method under possible decorators chain started from `object`.
        """
        self.name = name
        self.object_ = object_
        self.class_ = class_
        self.method = find_decorated_method(function=object_)
        self.type = self.get_type() if type_ is None else type_

    @property
    def unique_name(self):
        """
        Get unique name of the class member based on name and type.
        """
        return self.type + self.name

    @property
    def access_type(self):
        """
        Get member access modifier type.

        Variants are the followings: public, private, protected.
        """
        return self.get_access_type()

    @property
    def arguments(self):
        """
        Get class member arguments as tuple.
        """
        return self.get_arguments(function=self.method)

    @property
    def arguments_as_string(self):
        """
        Get class member arguments as string.

        Used for string formation.
        """
        return ', '.join(self.arguments)

    def get_property_arguments(self, property):
        """
        Get property arguments.

        If property is getter or deleter, the fetched arguments are single argument of
        class instance reference (e.g `self`).

        If property is setter, the arguments as string looks like `self, value`. To return it as tuple, blank symbols
        should be removed and return should be splitted by comma.
        """
        property_source_code = inspect.getsource(property)
        _, code_after_open_bracket = property_source_code.split('(')
        arguments_as_string, _ = code_after_open_bracket.split(')')

        if self.type == ClassMemberTypes.GETTER or self.type == ClassMemberTypes.DELETER:
            return (arguments_as_string, )

        arguments_as_string = arguments_as_string.replace(' ', '')
        arguments_as_tuple = tuple(arguments_as_string.split(','))

        return arguments_as_tuple

    def get_arguments(self, function):
        """
        Get class member arguments.

        `function.__code__.co_varnames` returns unordered function arguments.
        `function.__code__.co_varnames` returns all function arguments as expected in order of declaration.

        `inspect.signature` returns unordered function arguments.
        `inspect.signature` does not return `cls` (or another name for reference to class) in the function arguments.

        `__self__` is the class instance object. If class instance object is a class itself, so the method os static
        method.

        References:
            - https://docs.python.org/3/reference/datamodel.html
            - https://docs.python.org/3/library/inspect.html
        """
        if self.type == ClassMemberTypes.GETTER:
            return self.get_property_arguments(self.method.fget)

        if self.type == ClassMemberTypes.SETTER:
            return self.get_property_arguments(self.method.fset)

        if self.type == ClassMemberTypes.DELETER:
            return self.get_property_arguments(self.method.fdel)

        ordered_arguments = tuple(inspect.signature(function).parameters)
        first_argument, *_ = function.__code__.co_varnames

        if hasattr(function, ClassMemberMagicMethodNames.SELF) and function.__self__ == self.class_:
            return (first_argument, ) + ordered_arguments

        return ordered_arguments

    def get_type(self):
        """
        Get class member type.

        Variants are the followings: method, static method, class method.
        """
        method_source_code = inspect.getsource(self.method)

        if COMMERCIAL_AT_SYMBOL + ClassMemberTypes.CLASS_METHOD in method_source_code:
            return ClassMemberTypes.CLASS_METHOD

        if COMMERCIAL_AT_SYMBOL + ClassMemberTypes.STATIC_METHOD in method_source_code:
            return ClassMemberTypes.STATIC_METHOD

        return ClassMemberTypes.METHOD

    def get_access_type(self):
        """
        Get class member access modifier type.

        Variants are the followings: public, private, protected.
        """
        if isinstance(self.object_, property):
            return AccessModifierTypes.PUBLIC

        if self.object_.__name__ == 'private_wrapper':
            return AccessModifierTypes.PRIVATE

        if self.object_.__name__ == 'protected_wrapper':
            return AccessModifierTypes.PROTECTED

        return AccessModifierTypes.PUBLIC


def get_class_members(class_):
    """
    Get a list of the class members like functions, properties, etc.
    """
    inspected_members = {}

    class_members_ = \
        inspect.getmembers(class_, predicate=inspect.isfunction) + \
        inspect.getmembers(class_, predicate=inspect.ismethod)

    for member_name, member_object in class_members_:
        member = ClassMember(name=member_name, object_=member_object, class_=class_)
        inspected_members[member.unique_name] = member

    class_properties = inspect.getmembers(class_, predicate=isprop)

    for property_name, property_object in class_properties:
        member = \
            ClassMember(name=property_name, object_=property_object, class_=class_, type_=ClassMemberTypes.GETTER)
        inspected_members[member.unique_name] = member

        if property_object.fset is not None:
            member = \
                ClassMember(name=property_name, object_=property_object, class_=class_, type_=ClassMemberTypes.SETTER)
            inspected_members[member.unique_name] = member

        if property_object.fdel is not None:
            member = \
                ClassMember(name=property_name, object_=property_object, class_=class_, type_=ClassMemberTypes.DELETER)
            inspected_members[member.unique_name] = member

    return inspected_members


def get_method_class_by_frame(frame):
    """
    Get method's class by method's caller frame.

    Get method's caller frame items (in example {'Tesla': <object ...>}) and method's caller name.
    Browse all items in loop. If method's caller contains a member with method's caller name —
    we have found the class (`Tesla`) that contains the method (`run`) that calls a method (`start_engine`)
    with accessibility level.
    Check if founded method code is the code from frame (`start_engine` caller frame). If they are equal,
    method class is pointed as latest. Latest is returned, else None.

    # services/generic.py
    class Car:

        @private
        def start_engine(self):
            ...

    # __main__.py
    class Tesla:

        def run(self):
            car = Car()
            return car.start_engine()

    Latest object exists because if `Car` and `Tesla` will be in one file, both of these classes
    could have the same method that call protected method and function won't understand
    the real caller.

    # __main__.py
    class Car:

        @protected
        def start_engine(self):
            ...

        def run(self)
            return self.start_engine()

    class Tesla(Car):

        def run(self):
            return self.start_engine()
    """
    latest_object = None

    for name, object_ in frame.f_globals.items():

        try:
            class_method = object_.__dict__.get(frame.f_code.co_name)

            if class_method is not None:
                method = find_decorated_method(function=class_method)

                if method.__code__ is frame.f_code:
                    latest_object = object_

        except (KeyError, AttributeError):
            pass

    return latest_object
