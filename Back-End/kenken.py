
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

    def validate(size, cliques):
        outOfBounds = lambda xy: xy[0] < 1 or xy[0] > size or xy[1] < 1 or xy[1] > size

        mentioned = set()
        for i in range(len(cliques)):
            members, operator, target = cliques[i]
            cliques[i] = (tuple(set(members)), operator, target)
            members, operator, target = cliques[i]
            if operator not in "+-*/.":
                print("Operation", operator, "of clique", cliques[i], "is unacceptable", file=stderr)
                exit(1)

            problematic = list(filter(outOfBounds, members))
            if problematic:
                print("Members", problematic, "of clique", cliques[i], "are out of bounds", file=stderr)
                exit(2)

            problematic = mentioned.intersection(set(members))
            if problematic:
                print("Members", problematic, "of clique", cliques[i], "are cross referenced", file=stderr)
                exit(3)

            mentioned.update(set(members))
        indexes = range(1, size + 1)
        problematic = set([(x, y) for y in indexes for x in indexes]).difference(mentioned)

        if problematic:
            print("Positions", problematic, "were not mentioned in any clique", file=stderr)
            exit(4)

    def RowXorCol(xy1, xy2):
        return (xy1[0] == xy2[0]) != (xy1[1] == xy2[1])

    def conflicting(A, a, B, b):
        for i in range(len(A)):
            for j in range(len(B)):
                mA = A[i]
                mB = B[j]

                ma = a[i]
                mb = b[j]
                if generateKenkenPuzzle.RowXorCol(mA, mB) and ma == mb:
                    return True

        return False

    def satisfies(values, operation, target):
        for p in permutations(values):
            if reduce(operation, p) == target:
                return True

        return False

    def gdomains(size, cliques):
        domains = {}
        for clique in cliques:
            members, operator, target = clique
            domains[members] = list(product(range(1, size + 1), repeat=len(members)))
            qualifies = lambda values: not generateKenkenPuzzle.conflicting(members, values, members, values) and generateKenkenPuzzle.satisfies(values, generateKenkenPuzzle.operation(operator), target)
            domains[members] = list(filter(qualifies, domains[members]))
        return domains

    def gneighbors(cliques):
        neighbors = {}
        for members, _, _ in cliques:
            neighbors[members] = []

        for A, _, _ in cliques:
            for B, _, _ in cliques:
                if A != B and B not in neighbors[A]:
                    if generateKenkenPuzzle.conflicting(A, [-1] * len(A), B, [-1] * len(B)):
                        neighbors[A].append(B)
                        neighbors[B].append(A)

        return neighbors


class kenkenGame(csp.CSP):

    def __init__(self, size, cliques):
        generateKenkenPuzzle.validate(size, cliques)
        variables = [members for members, _, _ in cliques]
        domains = generateKenkenPuzzle.gdomains(size, cliques)
        neighbors = generateKenkenPuzzle.gneighbors(cliques)
        csp.CSP.__init__(self, variables, domains, neighbors, self.constraint)
        self.size = size
        self.checks = 0
        self.padding = 0
        self.meta = {}
        for members, operator, target in cliques:
            self.meta[members] = (operator, target)
            self.padding = max(self.padding, len(str(target)))        


    def constraint(self, A, a, B, b):
        self.checks += 1
        return A == B or not generateKenkenPuzzle.conflicting(A, a, B, b)


    def get_result_arr(self, assignment):
        if assignment:
            atomic = {}
            for members in self.variables:
                values = assignment.get(members)
                if values:
                    for i in range(len(members)):
                        atomic[members[i]] = values[i]
                else:
                    for member in members:
                        atomic[member] = None
        else:
            atomic = {member:None for members in self.variables for member in members}

        atomic = sorted(atomic.items(), key=lambda item: item[0][1] * self.size + item[0][0])

        global result_arr 
        result_arr = []
        for i in range (len(atomic)):
            result_arr.append(atomic[i][1])
        return result_arr


    def gui_border_configurations(cliques_gui,size):
        global top
        global bottom
        global left
        global right
        top=0
        bottom=1
        left=2
        right=3
        remove_border = [[[0 for i in range(4)] for j in range(size)]for k in range(size)]
        operation = [[[ '0' for i in range(1)] for j in range(size)]for k in range(size)]
        for i in range (len(cliques_gui)):
            operator_box=999
            operation_string = ''
            if(cliques_gui[i][-2]=='-' and cliques_gui[i][-1] < 0):
                operation_string = '+'+str(cliques_gui[i][-1])[1:]
            else:
                operation_string=str(cliques_gui[i][-2])+str(cliques_gui[i][-1])
            if(len(cliques_gui[i][0]) == 1):
                operator_box= [cliques_gui[i][0][0][0]-1,cliques_gui[i][0][0][1]-1]
            for j in range (len(cliques_gui[i][0])-1):
                pos1 = [cliques_gui[i][0][j][0]-1,cliques_gui[i][0][j][1]-1]
                if operator_box == 999:
                    operator_box=pos1

                for k in range(j+1,len(cliques_gui[i][0])):
                    pos2 = [cliques_gui[i][0][k][0]-1,cliques_gui[i][0][k][1]-1]
                    if(pos1[0] == pos2[0] or pos1[1] == pos2[1]):
                        if pos1[0] != pos2[0] and ((pos1[0] == pos2[0]-1) or (pos1[0] == pos2[0]+1)):
                            if(pos1[0]<pos2[0]):
                                remove_border[pos1[0]][pos1[1]][bottom]=1
                                remove_border[pos2[0]][pos2[1]][top]=1
                                if(operator_box[0] > pos1[0] ):
                                    operator_box=pos1
                            if(pos1[0]>pos2[0]):
                                remove_border[pos1[0]][pos1[1]][top]=1
                                remove_border[pos2[0]][pos2[1]][bottom]=1
                                if(operator_box[0] > pos2[0] ):
                                    operator_box=pos2
                
                        if(pos1[1] != pos2[1] and ((pos1[1] == pos2[1]-1) or (pos1[1] == pos2[1]+1))):
                            if(pos1[1]<pos2[1]):
                                remove_border[pos1[0]][pos1[1]][right]=1
                                remove_border[pos2[0]][pos2[1]][left]=1
                            if(pos1[1]>pos2[1]):
                                remove_border[pos1[0]][pos1[1]][left]=1
                                remove_border[pos2[0]][pos2[1]][right]=1
            operation[operator_box[0]][operator_box[1]] = operation_string
        return operation, remove_border
     
        
    def puzzleToDictionary(remove_border,operation):
        api_result = {}
        values= []
        for row in remove_border:
            for col in row:
                borders={
                    'top':col[0],
                    'bottom':col[1],
                    'left':col[2],
                    'right':col[3]
                }
                values.append(borders)
                
        op=[]
        for row in operation:
            for col in row:
                if col==['0']:
                    op.append('0')
                elif col[0]=='.':
                    op.append('*' + col[1:])
                else:
                    op.append(col)      
        for index,value in enumerate(op):
            values[index]['value']=value
        api_result['values']= values
        return api_result


    def answerToDictionary(result):
        api_result = {
            'result': result,
        }
        return api_result


    def benchmark(kenken, algorithm):
            kenken.checks = kenken.nassigns = 0
            dt = time()
            assignment = algorithm(kenken)
            dt = time() - dt
            return assignment, (kenken.checks, kenken.nassigns, dt)


    def gather(iterations,start_size,end_size,out):
        if start_size < 3:
            start_size = 3

        bt         = lambda ken: csp.CSP.backtracking_search(ken)
        fc         = lambda ken: csp.CSP.backtracking_search(ken, inference=csp.CSP.forward_checking)
        mac        = lambda ken: csp.CSP.backtracking_search(ken, inference=csp.CSP.mac)

        algorithms = {
            "Backtracking": bt,
            "Forward Checking": fc,
            "Arc Consistency": mac,
        }

        with open(out, "w+") as file:

            out = writer(file)

            out.writerow(["Algorithm", "Size", "Number of Tests Boards", "Average Completion time"])

            for name, algorithm in algorithms.items():
                for size in range(start_size, end_size+1):
                    checks, assignments, dt = (0, 0, 0)
                    for iteration in range(1, iterations + 1):
                        cliques = generateKenkenPuzzle.generate(size)

                        assignment, data = kenkenGame.benchmark(kenkenGame(size, cliques), algorithm)

                        print("algorithm =",  name, "size =", size, "iteration =", iteration, "result =", "Success" if assignment else "Failure", file=stderr)

                        checks      += data[0] / iterations
                        assignments += data[1] / iterations
                        dt          += data[2] / iterations
                        
                    out.writerow([name, size, iterations, dt])



