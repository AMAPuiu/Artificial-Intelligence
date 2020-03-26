
# 231 Puiu Ana

from copy import deepcopy

class Node:

    def __init__(self, data, level, fval, parent):
        self.data = data
        self.level = level
        self.fval = fval
        self.parent_info = parent

    def __str__ (self):
        return "({}, level={}, fval={})".format(self.data, self.level, self.fval)

    def generate_child(self):
        children = []
        config = list(self.data)

        for index in range(len(config)):

            if len(config[index]) > 0:
                for index2 in range(len(config)):
                    # Se muta ultimul element de pe o stiva pe cate o alta stiva
                    if index !=  index2:
                        new_config = deepcopy(config)
                        x = new_config[index].pop()
                        new_config[index2].append(x)
                        child_node = Node(new_config, self.level + 1, 0, self)
                        children.append(child_node)

        return children
    
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
        self.init_config = [['a'], ['c', 'b'], ['d']]
        self.final_config = [['b', 'c'], [], ['d', 'a']]
        # self.init_config = [['c', 'd'], [], ['a', 'b']]
        # self.final_config = [['c'], [], ['a']]

class Blocks:

    def __init__(self, problema):
        self.open = []
        self.closed = []
        self.problem = problema

    # Se calculeaza f
    def f(self, start, goal):
        return self.h(start.data, goal) + start.level

    def h(self, start, goal):
        # h = numarul de diferente intre configuratia actuala si cea finala 
        dif = 0
        for index in range(len(start)):
            dif += max(len(start[index]), len(goal[index])) - min(len(start[index]), len(goal[index]))
            for i in range(min(len(start[index]), len(goal[index]))):
                if start[index][i] != goal[index][i]:
                    dif += 1 
        return dif

    def search_list(self, l, node):
        for item in l:
            if node.data == item.data:
                return item
        return None

    # Algoritm
    def process(self):
        start = self.problem.init_config
        goal = self.problem.final_config

        start = Node(start, 0, 0, None)    
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
            children = nod_curent.generate_child()
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