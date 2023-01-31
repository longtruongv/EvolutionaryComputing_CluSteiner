import utils.constants as constants

class Graph:
    def __init__(self, filename):
        file = open(f"res\\input\\{filename}", "r")
        line = file.readline()

        while line:
            splitted = line.split(':')

            if "Name" in splitted[0]:
                self.name = splitted[1]
            elif "TYPE" in splitted[0]:
                self.type = splitted[1]
            elif "DIMENSION" in splitted[0]:
                self.dimension = int(splitted[1].strip())
                self.edge_weight = [[] for _ in range(self.dimension)]
            elif "NUMBER_OF_CLUSTERS" in splitted[0]:
                self.num_cluster = int(splitted[1].strip())
                self.clusters = [[] for _ in range(self.num_cluster)]
            elif "EDGE_WEIGHT_SECTION" in splitted[0]:
                for i in range(self.dimension):
                    line = file.readline()
                    splitted = line.split()
                    self.edge_weight[i] = [int(w.strip()) for w in splitted]   
            elif "CLUSTER_SECTION" in splitted[0]:
                self.steiner_vertexes = [i for i in range(self.dimension)]
                for i in range(self.num_cluster):
                    line = file.readline()
                    splitted = line.split()
                    for j in range(1, len(splitted)-1):
                        vertex = int(splitted[j].strip()) - 1
                        self.clusters[i].append(vertex)
                        self.steiner_vertexes.remove(vertex)

                self.num_steiner_vertexes = len(self.steiner_vertexes)
    
            line = file.readline()
        
        file.close()

    def calcu_weight(self, edge_matrix):
        if len(edge_matrix) != self.dimension:
            print("CALCU WEIGHT INVALID")
            return constants.MAX_INT

        total = 0
        for i in range(self.dimension):
            for j in range(i):
                if edge_matrix[i][j]:
                    total += self.edge_weight[i][j]

        return total


