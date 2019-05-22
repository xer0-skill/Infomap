import random
from math import log2
from random import sample
import random_walk

class Infomap:
    def __init__(self, graph):
        self.__graph = graph
        self.__number_clusters = 0
        self.__codelength = 0
        self.__visits_probabilities = {}
        self.__clusters_partition = dict.fromkeys(graph.keys(), 0)
        self.__number_iterations = len(graph)

    def clusters_reassignment(self, clusters_partition):
        new_clusters = dict()
        count = 0
        for node in clusters_partition.keys():
            cluster = clusters_partition[node]
            new_cluster = new_clusters.get(cluster)
            if  new_cluster is None:
                new_clusters[cluster] = count
                new_cluster = count
                count += 1
            clusters_partition[node] = new_cluster

    def calculate_map_equation(self, clusters_partition):
        number_clusters = len(set(clusters_partition.values()))
        q_in, index_codebook_entropy, conditional_clusters_entropy = (0, 0, 0)
        clusters_q_in, clusters_p_around, clusters_q_out = [[0 for i in range(number_clusters)] for j in range(3)]
        nodes_visits_entropy = [0 for i in range(number_clusters)]
        nodes_visits = dict.fromkeys(clusters_partition, 0)

        for node in clusters_partition:
            for neighbour in self.__visits_probabilities[node]:
                nodes_visits[neighbour] += self.__visits_probabilities[node][neighbour]
                clusters_p_around[clusters_partition[neighbour]] += self.__visits_probabilities[node][neighbour]
                nodes_visits_entropy[clusters_partition[neighbour]] += self.__visits_probabilities[node][neighbour]
                if clusters_partition[node] != clusters_partition[neighbour]:
                    clusters_p_around[clusters_partition[node]] += self.__visits_probabilities[node][neighbour]
                    clusters_q_out[clusters_partition[node]] += self.__visits_probabilities[node][neighbour]
                    clusters_q_in[clusters_partition[neighbour]] += self.__visits_probabilities[node][neighbour]
                    q_in += self.__visits_probabilities[node][neighbour]

        for node in clusters_partition:
            nodes_visits_entropy[clusters_partition[node]] += nodes_visits[node] * log2(nodes_visits[node]/clusters_p_around[clusters_partition[node]])

        for i in range(number_clusters):
            index_codebook_entropy -= clusters_q_in[i] * log2(clusters_q_in[i]/q_in)/q_in
            conditional_clusters_entropy -= clusters_q_out[i] * log2(clusters_q_out[i]/clusters_p_around[i]) + nodes_visits_entropy[i]

        return q_in * index_codebook_entropy + conditional_clusters_entropy

    def core_algorithm(self):
        rw = random_walk.RandomWalk(self.__graph)
        rw.walks(self.__graph)
        self.__visits_probabilities = rw.get_visits_probabilities()
        self.__number_clusters = len(self.__graph)

        current_clusters_partition = dict.fromkeys(self.__graph, 0)
        for cluster, node in zip(range(self.__number_clusters), self.__graph):
            current_clusters_partition[node] = cluster
        current_map_equation = self.calculate_map_equation(current_clusters_partition)
        current_number_clusters = len(self.__graph)
        best_clusters_partition = dict(current_clusters_partition)
        initial_clusters_partition = dict(current_clusters_partition)
        initial_map_equation = current_map_equation

        best_map_equation = current_map_equation
        for iteration in range(self.__number_iterations):
            for node in sample(self.__graph.keys(),len(self.__graph)):
                if current_number_clusters > 2:
                    current_map_equation = self.local_join(node, current_map_equation, current_clusters_partition)
                    current_number_clusters = len(set(current_clusters_partition.values()))

            if current_map_equation < best_map_equation:
                best_map_equation = current_map_equation
                best_clusters_partition = dict(current_clusters_partition)

            current_number_clusters = len(self.__graph)
            current_clusters_partition = dict(initial_clusters_partition)
            current_map_equation = self.calculate_map_equation(current_clusters_partition)

        self.__clusters_partition = best_clusters_partition
        self.__codelength = best_map_equation
        self.__number_clusters = len(set(best_clusters_partition.values()))
        print(self.__visits_probabilities)

    def local_join(self, node, cur_map_eq, cur_partition):
        cur_neighbour = None
        for neighbour in self.__graph[node]:
            if cur_partition[node] != cur_partition[neighbour]:
                temp_partition = dict(cur_partition)
                temp_cluster = temp_partition[node]
                for nodes_in_cluster in self.__graph:
                    if temp_partition[nodes_in_cluster] == temp_cluster:
                        temp_partition[nodes_in_cluster] = temp_partition[neighbour]

                self.clusters_reassignment(temp_partition)
                temp_map_equation = self.calculate_map_equation(temp_partition)
                if temp_map_equation < cur_map_eq:
                    cur_neighbour = neighbour
                    cur_map_eq = temp_map_equation

        was_moved = False
        if cur_neighbour is not None:
            temp_cluster = cur_partition[node]
            for nodes_in_cluster in self.__graph:
                if cur_partition[nodes_in_cluster] == temp_cluster:
                    cur_partition[nodes_in_cluster] = cur_partition[cur_neighbour]
            cur_partition[node] = cur_partition[cur_neighbour]
            self.clusters_reassignment(cur_partition)
            was_moved = True
        return cur_map_eq

    def get_clusters_partition(self):
        return self.__clusters_partition

    def get_number_clusters(self):
        return self.__number_clusters

    def get_codelength(self):
        return self.__codelength

    def set_visits_probabilities(self, visits_probabilities):
        self.__visits_probabilities = visits_probabilities
