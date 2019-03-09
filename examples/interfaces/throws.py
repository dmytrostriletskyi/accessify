from accessify import implements, throws


class HumanDoesNotExistsError(Exception):
    pass


class HumanAlreadyInLoveError(Exception):
    pass


class HumanInterface:

    @throws(HumanDoesNotExistsError, HumanAlreadyInLoveError)
    def love(self, who, *args, **kwargs):
        pass


if __name__ == '__main__':

    @implements(HumanInterface)
    class Human:

        def love(self, who, *args, **kwargs):

            if who is None:
                raise HumanDoesNotExistsError('Human whom need to love does not exist.')
