
import csp
from sys import stderr
from itertools import product, permutations
from functools import reduce
from random import random, shuffle, randint, choice
from time import time
from csv import writer

class generateKenkenPuzzle():
    def operation(operator):
        if operator == '+':
            return lambda a, b: a + b
        elif operator == '-':
            return lambda a, b: a - b
        elif operator == '*':
            return lambda a, b: a * b
        elif operator == '/':
            return lambda a, b: a / b
        else:
            return None

    

    
    



