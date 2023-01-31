import numpy as np

from graph import Graph
import utils.constants as constants

class Individual:
    def __init__(self, length:int=1):
        self.length = length
        self.chromosome = [-1 for _ in range(length)]
        self.fitness = constants.MIN_INT
        self.calculated = False

    def calcu_fitness(self, graph: Graph):
        if not self.calculated:
            self.calculated = True
            edge_matrix = self.decode(graph)
            total_weight = graph.calcu_weight(edge_matrix)
            self.fitness = 1 - total_weight

    def decode(self, graph: Graph):
        return decode(self, graph)

    def get(self, idx):
        if idx >= self.length:
            return None
        return self.chromosome[idx]

    def set(self, idx, gene):
        if idx >= self.length:
            return
        self.chromosome[idx] = gene

    def from_list(self, chromosome: list):
        self.length = len(chromosome)
        self.chromosome = chromosome
        


def decode(individual:Individual, graph:Graph):
    edge_matrix = [[False] * graph.dimension for _ in range(graph.dimension)]
    
    steiner_candidates = [x for _, x in sorted(
        zip(individual.chromosome, graph.steiner_vertexes), key=lambda pair: pair[0]
    )]

    new_clusters = [set() for _ in range(graph.num_cluster)]

    for i in range(graph.num_cluster):
        # print("CLUSTER")
        # print(steiner_candidates)
        selected_edges, steiner_candidates = __decode_intra_cluster(i, steiner_candidates, graph)
        
        new_clusters[i].add(graph.clusters[i][0])
        for v1, v2 in selected_edges:
            edge_matrix[v1][v2] = True
            edge_matrix[v2][v1] = True

            new_clusters[i].add(v1)
            new_clusters[i].add(v2)
        # print(new_clusters)
    # a, b = __decode_intra_cluster(0, [5,9,4], graph)
    # print(a)

    selected_edges = __decode_extra_cluster(new_clusters, steiner_candidates, graph)
    for v1, v2 in selected_edges:
            edge_matrix[v1][v2] = True
            edge_matrix[v2][v1] = True

    edge_matrix = __strip_steiner(edge_matrix, graph)
    return edge_matrix


# Prim
def __decode_intra_cluster(cluster_idx, steiner_candidates:list, graph:Graph):
    if cluster_idx > graph.num_cluster:
        return
    cluster = graph.clusters[cluster_idx].copy()

    visited = [cluster[0]]

    candidates = cluster[1:].copy()
    if len(steiner_candidates) > 0:
        candidates.append(steiner_candidates[0])

    selected_edges = []

    cluster.remove(cluster[0])
    while cluster:
        # print("LOOP")
        # print(cluster)
        # print(candidates)
        # print(steiner_candidates)
        min = constants.MAX_INT
        for v in visited:
            for cand in candidates:
                if graph.edge_weight[v][cand] < min:
                    min = graph.edge_weight[v][cand]
                    selected = (v, cand)

        selected_edges.append(selected)
        v, cand = selected
        # print(v, cand)

        visited.append(cand)
        candidates.remove(cand)

        if len(steiner_candidates) > 0 and cand == steiner_candidates[0]:
            steiner_candidates.pop(0)
            if len(steiner_candidates) > 0:
                candidates.append(steiner_candidates[0])
        else:
            cluster.remove(cand)

    return selected_edges, steiner_candidates


def __decode_extra_cluster(new_clusters:list[set], steiner_candidates:list, graph:Graph):
    egde_weight = np.array(graph.edge_weight)
    
    selected_edges = []

    visited = list(new_clusters[0])

    candidates = []
    for i in range(1, len(new_clusters)):
        candidates.extend(list(new_clusters[i]))
    if len(steiner_candidates) > 0:
        candidates.append(steiner_candidates[0])

    new_clusters.pop(0)
    while new_clusters:
        # print("LOOP 2")
        # print(visited)
        # print(candidates)
        # print(steiner_candidates)
        min = constants.MAX_INT
        for v in visited:
            for cand in candidates:
                if graph.edge_weight[v][cand] < min:
                    min = graph.edge_weight[v][cand]
                    selected = (v, cand)

        selected_edges.append(selected)
        v, cand = selected
        # print(v, cand)

        if len(steiner_candidates) > 0 and cand == steiner_candidates[0]:
            steiner_candidates.pop(0)

            visited.append(cand)
            candidates.remove(cand)
            if len(steiner_candidates) > 0:
                candidates.append(steiner_candidates[0])
        else:
            for i in range(len(new_clusters)):
                if cand in new_clusters[i]:
                    idx = i
            for v in new_clusters[idx]:
                visited.append(v)
                candidates.remove(v)
            new_clusters.pop(idx)

    return selected_edges
            
    
def __strip_steiner(edge_matrix, graph:Graph):
    for i in graph.steiner_vertexes:
        if sum(edge_matrix[i]) == 1:
            edge_matrix[i] = [False]*graph.dimension
            for row in edge_matrix:
                row[i] = False

    return edge_matrix

    