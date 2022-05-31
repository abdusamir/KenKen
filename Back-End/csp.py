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


# ...................
class CSP(Problem):

    def __init__(self, variables, domains, neighbors, constraints):
        variables = variables or list(domains.keys())

        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.curr_domains = None
        self.nassigns = 0

    def assign(self, var, val, assignment):
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]


