import pytest
import clustering
from two_level_infomap import Infomap
from random_walk import RandomWalk


def get_graphs_for_tests():
    graph1 = {'A':['B','C'],
            'B':['A','C'],
            'C':['A','B','D'],
            'D':['C','E','F'],
            'E':['D','F'],
            'F':['E','D']}
    graph2 = {0:[1,3],
            1:[0,2],
            2:[1,3,13],
            3:[0,2,4],
            4:[3,5,7],
            5:[4,6,8],
            6:[5,7],
            7:[4,6],
            8:[5,9,11],
            9:[8,10,12],
            10:[9,11],
            11:[8,10],
            12:[9,13,15],
            13:[2,12,14],
            14:[13,15],
            15:[12,14]}

    return (graph1, graph2)

def get_visits_probabilities(default_probabilities=(0.071, 0.025)):
    result = []
    graphs = get_graphs_for_tests()
    for i in range(len(graphs)):
        visits_probabilities = dict.fromkeys(graphs[i],{})
        for node in visits_probabilities:
            visits_probabilities[node] = dict.fromkeys(graphs[i], default_probabilities[i])
        result.append(visits_probabilities)

    return result

def get_partitions():
    partition1 = {'A':0,'B':0,'C':0,'D':1,'E':1,'F':1}
    partition2 = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5}
    return (partition1,partition2)

def get_incorrect_partitions():
    partition1 = {'A':4,'B':1,'C':1,'D':3,'E':3,'F':3}
    partition2 = {'A':0,'B':2,'C':3,'D':3,'E':5,'F':5}
    return (partition1,partition2)

def get_map_equations():
    map_eq1 = 1.325
    map_eq2 = 3.557
    return (map_eq1, map_eq2)


@pytest.mark.parametrize('eps, graph, partitions, map_equations',
                         [(0.2, get_graphs_for_tests()[0], get_partitions(), get_map_equations())])
def test_calculate_map_equation(eps, graph, partitions, map_equations):
    rw = RandomWalk(graph)
    rw.walks(graph)
    infomap = Infomap(graph)
    infomap.set_visits_probabilities(rw.get_visits_probabilities())
    for partition, map_eq in zip(partitions, map_equations):
        assert abs(infomap.calculate_map_equation(partition) - map_eq) <= eps


@pytest.mark.parametrize('eps, correct_new_map_eq, node, graph, partition, map_eq',
                         [(0.01, 3.0725, 'A', get_graphs_for_tests()[0]), get_partitions()[1], get_map_equations()[1]])
def test_local_join(eps, correct_new_map_eq, node, graph, partition, map_eq):
    rw = RandomWalk(graph)
    rw.walks(graph)
    infomap = Infomap(graph)
    infomap.set_visits_probabilities(rw.get_visits_probabilities())
    new_map_eq = infomap.local_join(node, map_eq, partition)
    assert partition['A'] == partition['B']
    assert abs(new_map_eq - correct_new_map_eq) <= eps


@pytest.mark.parametrize('test_graphs, incorrect_partitions',
                         [(get_graphs_for_tests(), get_incorrect_partitions())])
def test_clusters_reassignment(test_graphs, incorrect_partitions):
    for graph in test_graphs:
        infomap = Infomap(graph[0])
        for incorrect_partition in incorrect_partitions:
            infomap.clusters_reassignment(incorrect_partition)
            for i in range(len(set(incorrect_partition.values()))):
                assert i in incorrect_partition.values()


@pytest.mark.parametrize('eps, test_graphs, visits_probabilities',
                         [(0.01, get_graphs_for_tests(), get_visits_probabilities())])
def test_random_walk(eps, test_graphs, visits_probabilities):
    for graph, probabilities in zip(test_graphs, visits_probabilities):
        rw = RandomWalk(graph)
        rw.walks(graph)
        visits_probabilities = rw.get_visits_probabilities()
        for node in visits_probabilities:
            for neighbour in visits_probabilities[node]:
                assert abs(visits_probabilities[node][neighbour] - probabilities[node][neighbour]) <= eps


def get_solution_test_data():
    return [("solution_test1.txt", (('A', 'B', 'C'), ('D', 'E', 'F'))),
            ("solution_test2.txt", (('0', '1', '2', '3', '4', '5'), ('6', '7', '8', '9', '10', '11', '12'), ('13', '14', '15', '16'))),
            ("solution_test3.txt", (('0', '1', '2', '3'), ('4', '5', '6', '7'), ('8', '9', '10', '11'), ('12', '13', '14', '15')))]


@pytest.mark.parametrize('filename, expected_result', get_solution_test_data())
def test_solution_correctness(filename, expected_partition):
    clusters_partition = clustering.clustering(filename, file_output=False)
    for cluster in expected_partition:
        number = clusters_partition[cluster[0]]
        for node in cluster:
            assert clusters_partition[node] == number

    labels_clusters = []
    for cluster in expected_partition:
        assert clusters_partition[cluster[0]] not in labels_clusters
        labels_clusters.append(clusters_partition[cluster[0]])
