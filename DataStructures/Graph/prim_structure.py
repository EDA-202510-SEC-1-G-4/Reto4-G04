from DataStructures.List import array_list as al
from DataStructures.Queue import queue as qu
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Queue import queue as q
from DataStructures.Stack import stack as s
from DataStructures.Graph import digraph as G
from DataStructures.Priority_queue import index_priority_queue as ipq


def prim_mst(my_graph, source):
    search = {
        "edge_to": mp.new_map(1000),
        "dist_to": mp.new_map(1000),
        "marked": mp.new_map(1000),
        "pq": ipq.new_index_heap(True),
        "source": source,
        "mst": qu.new_queue()
    }

    vertices = G.vertices(my_graph)
    for i in range(al.size(vertices)):
        v = al.get_element(vertices, i)
        mp.put(search["dist_to"], v, float("inf"))
        mp.put(search["marked"], v, False)

    mp.put(search["dist_to"], source, 0)
    ipq.insert(search["pq"], 0, source)

    while not ipq.is_empty(search["pq"]):
        current = ipq.remove(search["pq"])
        mp.put(search["marked"], current, True)

        current_vertex = mp.get(my_graph["vertices"], current)
        adjacents = current_vertex["adjacents"]
        neighbors = mp.key_set(adjacents)

        for j in range(al.size(neighbors)):
            neighbor = al.get_element(neighbors, j)
            if mp.get(search["marked"], neighbor):
                continue

            edge = mp.get(adjacents, neighbor)
            weight = edge["weight"]
            current_dist = mp.get(search["dist_to"], neighbor)

            if weight is not None and weight < current_dist:
                mp.put(search["dist_to"], neighbor, weight)
                mp.put(search["edge_to"], neighbor, {"vertexA": current, "vertexB": neighbor, "weight": weight})
                if ipq.contains(search["pq"], neighbor):
                    ipq.decrease_key(search["pq"], neighbor, weight)
                else:
                    ipq.insert(search["pq"], weight, neighbor)

    return search


def edges_mst(my_graph, search):
    mst = qu.new_queue()
    keys = mp.key_set(search["edge_to"])
    for i in range(al.size(keys)):
        key = al.get_element(keys, i)
        edge = mp.get(search["edge_to"], key)
        q.enqueue(mst, edge)
    return mst


def weight_mst(my_graph, search):
    total_weight = 0
    keys = mp.key_set(search["edge_to"])
    for i in range(al.size(keys)):
        key = al.get_element(keys, i)
        edge = mp.get(search["edge_to"], key)
        weight = edge["weight"]
        if weight is not None:
            total_weight += weight
    return total_weight


def num_vertices(search):
    """
    Retorna el número de vértices en el MST construido por Prim.

    :param search: La estructura retornada por Prim
    :type search: dict

    :return: Número de vértices conectados en el MST
    :rtype: int
    """
    return mp.size(search["edge_to"]) + 1  # +1 para incluir el vértice fuente