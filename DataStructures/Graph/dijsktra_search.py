from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al
from DataStructures.Stack import stack as stk
from DataStructures.Graph import digraph as g
from DataStructures.Graph import dijsktra_structure as ds
from DataStructures.Priority_queue import index_priority_queue as ipq

def dijkstra(my_graph, source):
    order = g.order(my_graph)
    search = ds.new_dijsktra_structure(source, order)

    dist_to = mp.new_map(order)
    edge_to = mp.new_map(order)
    visited = mp.new_map(order)
    pq = ipq.new_index_heap(is_min_pq=True)

    vertices = g.vertices(my_graph)
    for v in vertices["elements"]:
        mp.put(dist_to, v, float("inf"))

    mp.put(dist_to, source, 0)
    ipq.insert(pq, 0, source)

    while not ipq.is_empty(pq):
        u = ipq.remove(pq)
        mp.put(visited, u, True)

        u_vertex = mp.get(my_graph["vertices"], u)
        adj = u_vertex["adjacents"]
        keys = mp.key_set(adj)

        for v in keys["elements"]:
            edge = mp.get(adj, v)
            weight = edge["weight"]
            alt = mp.get(dist_to, u) + weight
            if alt < mp.get(dist_to, v):
                mp.put(dist_to, v, alt)
                mp.put(edge_to, v, u)
                if ipq.contains(pq, v):
                    ipq.decrease_key(pq, v, alt)
                else:
                    ipq.insert(pq, alt, v)

    search["dist_to"] = dist_to
    search["edge_to"] = edge_to
    search["visited"] = visited
    search["pq"] = pq

    return search

def has_path_to(vertex, search):
    return mp.contains(search["dist_to"], vertex) and mp.get(search["dist_to"], vertex) < float("inf")

def dist_to(vertex, search):
    if not has_path_to(vertex, search):
        return float("inf")
    return mp.get(search["dist_to"], vertex)

def path_to(vertex, search):
    if not has_path_to(vertex, search):
        return None
    path = stk.new_stack()
    current = vertex
    while current != search["source"]:
        stk.push(path, current)
        current = mp.get(search["edge_to"], current)
    stk.push(path, search["source"])
    return path