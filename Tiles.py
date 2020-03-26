
# 231 Puiu Ana

from copy import deepcopy

class Node:

    def __init__(self, data, gval, fval, parent):
        self.data = data
        self.gval = gval
        self.fval = fval
        self.parent_info = parent

    def __str__ (self):
        return "({}, gval={}, fval={})".format(self.data, self.gval, self.fval)
    
    # Calculare g - costul de a elimina = costul parintelui + 1 + (n - k) / n,
    #  unde n - nr de placute "symbol" din parinte si k - nr de placute "symbol" eliminate 
    def g(self, config, symbol):
        nr_type = 0
        nr_remained_type = 0
        for line in config:
            for col in line:
                if col == symbol:
                    nr_type += 1
        for line in self.data:
            for col in line:
                if col == symbol:
                    nr_remained_type += 1
        return 1 + nr_remained_type/nr_type + self.parent_info.gval

    # Cautare zone de placute ce acelasi tip
    def find_areas(self, config):
        available_positions = [(i, j) for i in range(len(config)) for j in range(len(config[0]))]
        available_areas = []
        while len(available_positions) > 0:
            area = []
            area.append(available_positions.pop(0))

            if config[area[0][0]][area[0][1]] != "#":
                for (poz_l, poz_c) in area:

                    if poz_l + 1 < len(config) and config[poz_l + 1][poz_c] == config[poz_l][poz_c]:
                        area.append((poz_l + 1, poz_c))
                        if (poz_l + 1, poz_c) in available_positions:
                            available_positions.remove((poz_l + 1, poz_c))

                    if poz_c + 1 < len(config[0]) and config[poz_l][poz_c + 1] == config[poz_l][poz_c]:
                        area.append((poz_l, poz_c + 1))
                        if (poz_l, poz_c + 1) in available_positions:
                            available_positions.remove((poz_l, poz_c + 1))

                if len(area) >= 3:
                    available_areas.append(area)

        return available_areas
    
    # Generarea unor matrici noi prin eliminarea unor zone
    def generate_new_config(self, config, area):
        new_config = deepcopy(config)
        nr_lines = len(config)
        nr_col = len(config[0])
        for (poz_l, poz_c) in area:
            new_config[poz_l][poz_c] = '#'
        
        for col in range(nr_col):
            non_empty = ['#'] * nr_lines
            poz = 0
            for line in range(nr_lines - 1, -1, -1):
                if new_config[line][col] != '#':
                    non_empty[poz] = new_config[line][col]
                    poz += 1

            for line in range(nr_lines - 1, -1, -1):
                new_config[line][col] = non_empty[nr_lines - 1 - line]

        for col in range(nr_col):
            is_empty = True
            for line in range(nr_lines):
                if new_config[line][col] != '#':
                    is_empty = False
            if is_empty == True:
                for next_col  in range(col + 1, nr_col):
                    for line in range(nr_lines):
                        new_config[line][next_col - 1], new_config[line][next_col] = new_config[line][next_col - 1], new_config[line][next_col]

        return new_config

    # Generarea nodurilor succesor

    def generate_child(self):
        children = []
        config = list(self.data)

        available_areas = self.find_areas(config)
        
        for area in available_areas:
            
            child = Node(self.generate_new_config(config, area), 0, 0, self)
            child.gval = child.g(config, config[area[0][0]][area[0][1]])
            children.append(child)

        return children

    def print_matrix(self, matrix, g):
        s = ""
        for line in matrix:
            for col in line:
                s += str(col) + " "
            s += "\n"
        g.write(s)
        g.write("\n")
        print(s)
                
    def print_sol(self, init_config):
        g = open("output.txt", "w")
        nod_c = self
        drum = [nod_c]
        while nod_c.data != init_config:
            drum = [nod_c.parent_info] + drum
            nod_c = nod_c.parent_info
        
        self.print_matrix(drum[0].data, g)
        cost_tata = drum[0].gval
        for x in drum[1:]:
            self.print_matrix(x.data, g)
            print(f"Cost mutare: {x.gval - cost_tata}.")
            g.write(f"Cost mutare: {x.gval - cost_tata}.")
            cost_tata = x.gval
            print("\n")
            g.write("\n")
        print(f"S-au realizat {len(drum) - 1} mutari cu costul {drum[-1].gval}.")
        g.write("\n")
        g.write(f"S-au realizat {len(drum) - 1} mutari cu costul {drum[-1].gval}.")
        g.close()


class Problem:
    # Problema
    def __init__(self):
        self.init_config = [['a', 'a', 'a', 'a'], ['a', 'b', 'b', 'b'], ['c', 'c', 'c', 'c'], ['a', 'a', 'a', 'a']]
        self.final_config = [['#', '#', '#', '#'], ['#', '#', '#', '#'], ['#', '#', '#', '#'], ['#', '#', '#', '#']]
        # self.init_config = [['a', 'a', 'a'], ['a', 'b', 'b'], ['c', 'c', 'c'], ['a', 'a', 'a']]
        # self.final_config = [['#', '#', '#'], ['#', '#', '#'], ['#', '#', '#'], ['#', '#', '#']]

    def read_input(self):
        f = open("input.txt")
        lines = f.read().split("\n")
        matrix = [ [item for item in line.split(" ")] for line in lines]
        self.init_config = matrix
        f.close()

class Grid:

    def __init__(self, problema):
        self.open = []
        self.closed = []
        self.problem = problema

    # Se calculeaza f
    def f(self, start, goal):
        return self.h(start.data, goal) + start.gval

    def h(self, start, goal):
        # h = numarul de placi ramase
        
        # nr_placi = 0
        # for line in start:
        #     for col in line:
        #         if col != '#':
        #             nr_placi += 1
        
        # return nr_placi
        

        #sau

        # h = numarul de zone ramase 
        x = Node(None, 0, 0, None)
        areas = []
        areas = x.find_areas(start)
        return len(areas)


    def search_list(self, l, node):
        for item in l:
            if node.data == item.data:
                return item
        return None

    # Algoritm
    def process(self):
        start = self.problem.init_config
        goal = self.problem.final_config

        start_node = Node(start, 0, 0, None)    
        start_node.fval = self.f(start_node,goal)
        self.open.append(start_node)

        print("\n\n")

        while len(self.open) > 0:
            print("Open:\n")
            for node in self.open:
                print(str(node))

            print('\n')

            nod_curent = self.open.pop(0)	
            self.closed.append(nod_curent)

            # Verificare nod scop
            if(nod_curent.data == goal):
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
                        old_child.gval = child.gval
                        nod_nou = old_child	
                else :
                    # Daca este in open                    
                    old_child_open = self.search_list(self.open, child)

                    if old_child_open is not None:
                        if child.fval < old_child_open.fval:
                            self.open.remove(old_child_open)
                            old_child_open.parent = nod_curent 
                            old_child_open.fval = child.fval
                            old_child.gval = child.gval
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
                            while i < len(self.open) and self.open[i].fval == nod_nou.fval and self.open[i].gval > nod_nou.gval:
                                i += 1
                            break

                    self.open.insert(i, nod_nou)

        print("\n------------------ Concluzie -----------------------")
        if len(self.open) == 0:
            print("Nu avem solutie.")
            g = open("output.txt", "w")
            g.write("Nu avem solutie.")
            g.close()
        else:
            nod_curent.print_sol(self.problem.init_config)


if __name__ == "__main__":
    problema = Problem()
    problema.read_input()
    grid = Grid(problema)
    grid.process()