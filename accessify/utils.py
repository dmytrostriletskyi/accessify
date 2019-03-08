"""
Provide utils.
"""
import inspect

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


class ClassMemberDefaultArguments:
    """
    Provide class members arguments default values.
    """

    SELF = 'self'
    CLS = 'cls'


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


def does_parents_contain_private_method(classes, method):
    """
    Check if at least one of parent classes contain method.

    Rules:
        - if classes first element is object, so obviously return false,
        - if class parents contain the method (called by child) and this method has private access level, return true.
    """
    if classes[0].__name__ == 'object':
        return False, None

    for class_ in classes:
        if hasattr(class_, method.__name__):
            if getattr(class_, method.__name__).__name__ in ACCESS_WRAPPERS_NAMES:
                return True, class_

    return False, None


def find_decorated_method(function):
    """
    Return the method going from the most top placed decorator under it.
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

    Used for inspect built-in Python module.

    References:
        - https://docs.python.org/3/library/inspect.html.
    """
    return isinstance(object_, property)


class ClassMember:
    """
    Provide implementation of class member.
    """

    def __init__(self, class_, method_info, type_=None):
        """
        Constructor.
        """
        self.name, self.highest_decorator_function = method_info

        self.class_ = class_
        self.method = find_decorated_method(function=self.highest_decorator_function)

        self.type = self.get_type(class_=self.class_, function=self.method) if type_ is None else type_

    @property
    def arguments_as_string(self):
        """
        Get arguments as string.

        Used for string formation.
        """
        arguments_as_tuple = self.get_arguments(class_=self.class_, function=self.method)
        arguments_as_string = ', '.join(arguments_as_tuple)
        return arguments_as_string

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
        """
        return self.get_access_type()

    @staticmethod
    def get_property_setter_argument_name(property_setter):
        """
        Get property setter argument name.
        """
        source_code = inspect.getsource(property_setter)

        _, after_self_argument_source_code = source_code.split(',')
        argument_after_self, _ = after_self_argument_source_code.split(')')

        return argument_after_self.strip()

    def get_arguments(self, class_, function):
        """
        Get function arguments.
        """
        if self.type == ClassMemberTypes.DELETER or self.type == ClassMemberTypes.GETTER:
            return ClassMemberDefaultArguments.SELF,

        if self.type == ClassMemberTypes.SETTER:
            property_setter_argument_name = self.get_property_setter_argument_name(self.method.fset)
            return ClassMemberDefaultArguments.SELF, property_setter_argument_name,

        arguments = tuple(inspect.signature(function).parameters)

        first_function_argument, *_ = arguments

        if hasattr(function, ClassMemberMagicMethodNames.SELF) and function.__self__ == class_:
            return (ClassMemberDefaultArguments.CLS,) + arguments

        return arguments

    @staticmethod
    def get_type(class_, function):
        """
        Get member type.

        Variants the followings: method, static method, class method.
        """
        arguments = tuple(inspect.signature(function).parameters)

        first_function_argument, *_ = arguments

        if first_function_argument == ClassMemberDefaultArguments.SELF:
            return ClassMemberTypes.METHOD

        if first_function_argument == ClassMemberDefaultArguments.CLS:
            return ClassMemberTypes.CLASS_METHOD

        if hasattr(function, ClassMemberMagicMethodNames.SELF) and function.__self__ == class_:
            return ClassMemberTypes.CLASS_METHOD

        return ClassMemberTypes.STATIC_METHOD

    def get_access_type(self):
        """
        Get member access modifier type.
        """
        if isinstance(self.highest_decorator_function, property):
            return AccessModifierTypes.PUBLIC

        if self.highest_decorator_function.__name__ == 'private_wrapper':
            return AccessModifierTypes.PRIVATE

        if self.highest_decorator_function.__name__ == 'protected_wrapper':
            return AccessModifierTypes.PROTECTED

        return AccessModifierTypes.PUBLIC


def get_class_members(class_):
    """
    Get a list of the class members like function, properties, etc.
    """
    inspected_members = {}

    class_members_ = \
        inspect.getmembers(class_, predicate=inspect.isfunction) + \
        inspect.getmembers(class_, predicate=inspect.ismethod)

    for method_info in class_members_:
        member = ClassMember(class_=class_, method_info=method_info)
        inspected_members[member.unique_name] = member

    class_properties = inspect.getmembers(class_, predicate=isprop)

    for property_info in class_properties:
        _, property_ = property_info

        member = ClassMember(class_=class_, method_info=property_info, type_=ClassMemberTypes.GETTER)
        inspected_members[member.unique_name] = member

        if property_.fset is not None:
            member = ClassMember(class_=class_, method_info=property_info, type_=ClassMemberTypes.SETTER)
            inspected_members[member.unique_name] = member

        if property_.fdel is not None:
            member = ClassMember(class_=class_, method_info=property_info, type_=ClassMemberTypes.DELETER)
            inspected_members[member.unique_name] = member

    return inspected_members
