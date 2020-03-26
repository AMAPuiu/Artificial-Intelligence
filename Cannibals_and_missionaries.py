
# 231 Puiu Ana

from copy import deepcopy

class Node:

    def __init__(self, position, nr_can_est, nr_mis_est, nr_can_vest, nr_mis_vest, level, fval, parent):
        self.data = (position, nr_can_est, nr_mis_est, nr_can_vest, nr_mis_vest) 
        self.level = level
        self.fval = fval
        self.parent_info = parent

    def __str__ (self):
        return "({}, level={}, fval={})".format(self.data, self.level, self.fval)

    def generate_child(self, n, boat_size):
        children = []
        position = ''
        if self.data[0] == 'E':
            position = 'V'
            # Se iau toate posibilitatile de a pune oameni in barca
            for can_number in range(min(boat_size + 1, self.data[1] + 1)): 
                max_mis_number = min(boat_size - can_number, self.data[2])
                for mis_number in range(max_mis_number + 1):
                    # Daca barca poate pleca
                    if can_number + mis_number > 0 and (can_number <= mis_number or mis_number == 0): 
                        can_est = self.data[1] - can_number
                        mis_est = self.data[2] - mis_number
                        can_vest = self.data[3] + can_number
                        mis_vest = self.data[4] + mis_number
                        # Daca se pastreaza proportionalitatea pe cele doua maluri
                        if (can_est <= mis_est or mis_est == 0) and (can_vest <= mis_vest or mis_vest == 0): 
                            child = Node(position, can_est, mis_est, can_vest, mis_vest, self.level + 1, 0, self)
                            children.append(child)
        else:
            position = 'E'
            # Se iau toate posibilitatile de a pune oameni in barca
            for can_number in range(min(boat_size + 1, self.data[3] + 1)):
                max_mis_number = min(boat_size - can_number, self.data[4])
                for mis_number in range(max_mis_number + 1):
                    # Daca barca poate pleca
                    if can_number + mis_number > 0 and (can_number <= mis_number or mis_number == 0):
                        can_est = self.data[1] + can_number
                        mis_est = self.data[2] + mis_number
                        can_vest = self.data[3] - can_number
                        mis_vest = self.data[4] - mis_number
                        # Daca se pastreaza proportionalitatea pe cele doua maluri
                        if (can_est <= mis_est or mis_est == 0) and (can_vest <= mis_vest or mis_vest == 0):
                            child = Node(position, can_est, mis_est, can_vest, mis_vest, self.level + 1, 0, self)
                            children.append(child)

        return children

    # Printare solutie
    def print_sol(self, init_config):
        nod_c = self
        drum = [nod_c]
        while nod_c.data != init_config:
            drum = [nod_c.parent_info] + drum
            nod_c = nod_c.parent_info
        sir = "[ "
        for x in drum:
            sir += str(x) + "  "
        sir += "]"
        return sir


class Problem:
    # Problema
    def __init__(self):
        self.n = 2
        self.m = 2
        self.init_config = ('E', self.n, self.n, 0, 0)
        self.final_config = ('V', 0, 0, self.n, self.n)

class Blocks:

    def __init__(self, problema):
        self.open = []
        self.closed = []
        self.problem = problema
    # Calcularea lui f
    def f(self, start, goal):
        return self.h(start.data, goal) + start.level

    def h(self, start, goal):
        # h = nr persoane pe malul de est
        return start[1] + start[2]

    def search_list(self, l, node):
        for item in l:
            if node.data == item.data:
                return item
        return None

    # Algoritm
    def process(self):
        start = self.problem.init_config
        goal = self.problem.final_config

        start = Node('E', self.problem.n, self.problem.n, 0, 0, 0, 0, None)    
        start.fval = self.f(start,goal)
        self.open.append(start)

        print("\n\n")

        while len(self.open) > 0:
            print("Open:\n")
            for node in self.open:
                print(str(node))

            print('\n')
        
            nod_curent = self.open.pop(0)	
            self.closed.append(nod_curent)

            # Verificare nod scop
            if(self.h(nod_curent.data, goal) == 0):
                break
            # Generare succesori
            children = nod_curent.generate_child(self.problem.n, self.problem.m)
            for child in children:
                child.fval = self.f(child,goal)
                old_child = self.search_list(self.closed, child)
                nod_nou = None
                # Daca este in closed
                if old_child is not None:
                    if child.fval < old_child.fval:
                        self.closed.remove(old_child)
                        old_child.parent = nod_curent 
                        old_child.fval = child.fval	
                        nod_nou = old_child	
                else :
                    # Daca este in open
                    old_child_open = self.search_list(self.open, child)

                    if old_child_open is not None:
                        if child.fval < old_child_open.fval:
                            self.open.remove(old_child_open)
                            old_child_open.parent = nod_curent 
                            old_child_open.fval = child.fval
                            nod_nou = old_child_open

                    else: 
                        nod_nou = child

                if nod_nou:
                    # Actualizare open
                    i=0
                    while i < len(self.open):
                        if self.open[i].fval < nod_nou.fval:
                            i += 1
                        else:
                            while i < len(self.open) and self.open[i].fval == nod_nou.fval and self.open[i].level > nod_nou.level:
                                i += 1
                            break

                    self.open.insert(i, nod_nou)

        print("\n------------------ Concluzie -----------------------")
        if len(self.open) == 0:
            print("Lista open e vida, nu avem drum de la nodul start la nodul scop")
        else:
            print(nod_curent.print_sol(self.problem.init_config))


if __name__ == "__main__":
    problema = Problem()
    bloc = Blocks(problema)
    bloc.process()