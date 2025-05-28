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
        v = ipq.remove(search["pq"])
        mp.put(search["marked"], v, True)

        vertex = mp.get(my_graph["vertices"], v)
        adj = vertex["adjacents"]
        keys = mp.key_set(adj)
        for j in range(al.size(keys)):
            w = al.get_element(keys, j)
            edge = mp.get(adj, w)
            weight = edge["weight"]

            if mp.get(search["marked"], w):
                continue

            if weight < mp.get(search["dist_to"], w):
                mp.put(search["edge_to"], w, {"vertexA": v, "vertexB": w, "weight": weight})
                mp.put(search["dist_to"], w, weight)
                if ipq.contains(search["pq"], w):
                    ipq.decrease_key(search["pq"], w, weight)
                else:
                    ipq.insert(search["pq"], weight, w)

    return search


def edges_mst(my_graph, search):
    mst = q.new_queue()
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
        total_weight += edge["weight"]
    return total_weight