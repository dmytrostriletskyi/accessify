from accessify import implements


class HumanSoulInterface:

    def love(self, who, *args, **kwargs):
        pass


class HumanBasicsInterface:

    @staticmethod
    def eat(food, *args, allergy=None, **kwargs):
        pass


if __name__ == '__main__':

    @implements(HumanSoulInterface, HumanBasicsInterface)
    class Human:

        def love(self, who, *args, **kwargs):
            pass
