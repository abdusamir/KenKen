import random
from functools import reduce


class utilities():

    def count(seq):
        return sum(bool(x) for x in seq)

    def first(iterable, default=None):
        try:
            return iterable[0]
        except IndexError:
            return default
        except TypeError:
            return next(iterable, default)

    def is_in(elt, seq):
        return any(x is elt for x in seq)


