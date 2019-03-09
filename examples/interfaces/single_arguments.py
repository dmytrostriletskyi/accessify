from accessify import implements


class HumanInterface:

    @staticmethod
    def eat(food, *args, allergy=None, **kwargs):
        pass


if __name__ == '__main__':

    @implements(HumanInterface)
    class Human:

        @staticmethod
        def eat(food):
            pass
