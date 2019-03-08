"""
Provide tests for detection class members.
"""
from accessify.access import (
    private,
    protected,
)
from accessify.interfaces import (
    get_class_members,
)
from accessify.utils import (
    ClassMemberTypes,
    ClassMember,
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


def test_get_class_members():
    """
    Case: get members of the class.
    Expect: name, arguments and type as strings, function as object are returned composed to dicts.
    """
    expected_result = {}

    members = [
        ClassMember(
            class_=UserInterface,
            method_info=('love', UserInterface.love),
        ),
        ClassMember(
            class_=UserInterface,
            method_info=('name', UserInterface.name),
            type_=ClassMemberTypes.GETTER,
        ),
        ClassMember(
            class_=UserInterface,
            method_info=('name', UserInterface.name),
            type_=ClassMemberTypes.SETTER,
        ),
        ClassMember(
            class_=UserInterface,
            method_info=('name', UserInterface.name),
            type_=ClassMemberTypes.DELETER,
        ),
        ClassMember(
            class_=UserInterface,
            method_info=('eat', UserInterface.eat),
        ),
        ClassMember(
            class_=UserInterface,
            method_info=('think', UserInterface.think),
        ),
        ClassMember(
            class_=UserInterface,
            method_info=('dream', UserInterface.dream),
        ),
        ClassMember(
            class_=UserInterface,
            method_info=('die', UserInterface.die),
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
