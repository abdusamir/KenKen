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

class Problem(object):

    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        if isinstance(self.goal, list):
            return utilities.is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self, state):
        raise NotImplementedError
        
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


# **********
    def nconflicts(self, var, val, assignment):
        def conflict(var2):
            return (var2 in assignment and
                    not self.constraints(var, val, var2, assignment[var2]))
        return utilities.count(conflict(v) for v in self.neighbors[var])


    def result(self, state, action):
        (var, val) = action
        return state + ((var, val),)

    def goal_test(self, state):
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    def support_pruning(self):
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals



    def prune(self, var, value, removals):
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    
    def revise(csp, Xi, Xj, removals):
        revised = False
        for x in csp.curr_domains[Xi][:]:
            if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
                csp.prune(Xi, x, removals)
                revised = True
        return revised

    def first_unassigned_variable(assignment, csp):
        return utilities.first([var for var in csp.variables if var not in assignment])

    def unordered_domain_values(var, assignment, csp):
        return csp.choices(var)

    def no_inference(csp, var, value, assignment, removals):
        return True




    def backtracking_search(csp,
                            select_unassigned_variable=first_unassigned_variable,
                            order_domain_values=unordered_domain_values,
                            inference=no_inference):
        def backtrack(assignment):
            if len(assignment) == len(csp.variables):
                return assignment
            var = select_unassigned_variable(assignment, csp)
            for value in order_domain_values(var, assignment, csp):
                if 0 == csp.nconflicts(var, value, assignment):
                    csp.assign(var, value, assignment)
                    removals = csp.suppose(var, value)
                    if inference(csp, var, value, assignment, removals):
                        result = backtrack(assignment)
                        if result is not None:
                            return result
                    csp.restore(removals)
            csp.unassign(var, assignment)
            return None

        result = backtrack({})
        assert result is None or csp.goal_test(result)
        return result
