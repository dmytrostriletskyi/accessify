"""
Provide tests for getting class members.
"""
from accessify.access import (
    private,
    protected,
)
from accessify.interfaces import get_class_members
from accessify.utils import (
    ClassMember,
    ClassMemberTypes,
)
from tests.utils import custom_decorator


class UserInterface:

    def love(self, who, *args, **kwargs):
        pass

    @property
    def name(self):
        return

    @name.setter
    def name(self, new_name):
        return

    @name.deleter
    def name(self):
        return

    @staticmethod
    def eat(food, *args, allergy=None, **kwargs):
        pass

    @classmethod
    def think(cls, about, *args, **kwargs):
        pass

    @private
    @staticmethod
    @custom_decorator
    def dream(about, *args, **kwargs):
        pass

    @protected
    @classmethod
    @custom_decorator
    def die(cls, when, *args, **kwargs):
        pass


def test_get_class_members(enable_accessify):
    """
    Case: get members of the class.
    Expect: class member as class that contains name, arguments, arguments as strings, object reference, etc.
    """
    expected_result = {}

    members = [
        ClassMember(
            class_=UserInterface,
            name='love',
            object_=UserInterface.love,
        ),
        ClassMember(
            class_=UserInterface,
            name='name',
            object_=UserInterface.name,
            type_=ClassMemberTypes.GETTER,
        ),
        ClassMember(
            class_=UserInterface,
            name='name',
            object_=UserInterface.name,
            type_=ClassMemberTypes.SETTER,
        ),
        ClassMember(
            class_=UserInterface,
            name='name',
            object_=UserInterface.name,
            type_=ClassMemberTypes.DELETER,
        ),
        ClassMember(
            class_=UserInterface,
            name='eat',
            object_=UserInterface.eat,
        ),
        ClassMember(
            class_=UserInterface,
            name='think',
            object_=UserInterface.think,
        ),
        ClassMember(
            class_=UserInterface,
            name='dream',
            object_=UserInterface.dream,
        ),
        ClassMember(
            class_=UserInterface,
            name='die',
            object_=UserInterface.die,
        ),
    ]

    for member in members:
        expected_result.update({
            member.unique_name: member,
        })

    result = get_class_members(class_=UserInterface)

    for member_unique_name, member in result.items():
        expected_member = expected_result.get(member_unique_name)
        assert expected_member.__dict__ == member.__dict__
        assert expected_member.arguments == member.arguments
