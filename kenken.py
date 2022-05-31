
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

    def adjacent(xy1, xy2):
        x1, y1 = xy1
        x2, y2 = xy2
        dx, dy = x1 - x2, y1 - y2
        return (dx == 0 and abs(dy) == 1) or (dy == 0 and abs(dx) == 1)

    def generate(size):
        board = [[((i + j) % size) + 1 for i in range(size)] for j in range(size)]
        for _ in range(size):
            shuffle(board)

        for c1 in range(size):
            for c2 in range(size):
                if random() > 0.5:
                    for r in range(size):
                        board[r][c1], board[r][c2] = board[r][c2], board[r][c1]

        board = {(j + 1, i + 1): board[i][j] for i in range(size) for j in range(size)}
        uncaged = sorted(board.keys(), key=lambda var: var[1])

        global cliques
        cliques = []
        while uncaged:
            cliques.append([])
            csize = randint(1, 4)
            cell = uncaged[0]
            uncaged.remove(cell)
            cliques[-1].append(cell)
            for _ in range(csize - 1):
                adjs = [other for other in uncaged if generateKenkenPuzzle.adjacent(cell, other)]
                cell = choice(adjs) if adjs else None
                if not cell:
                    break

                uncaged.remove(cell)
                cliques[-1].append(cell)
            csize = len(cliques[-1])
            if csize == 1:
                cell = cliques[-1][0]
                cliques[-1] = ((cell, ), '.', board[cell])
                continue
            elif csize == 2:
                fst, snd = cliques[-1][0], cliques[-1][1]
                if board[fst] / board[snd] > 0 and not board[fst] % board[snd]:
                    operator = "/"
                else:
                    operator = "-"
            else:
                operator = choice("+*")

            target = reduce(generateKenkenPuzzle.operation(operator), [board[cell] for cell in cliques[-1]])

            cliques[-1] = (tuple(cliques[-1]), operator, int(target))

        return cliques

    



