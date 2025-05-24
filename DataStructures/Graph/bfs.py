from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Queue import queue as q
from DataStructures.Graph import digraph as G

def bfs(graph, source):
    if not G.contains_vertex(graph, source):
        raise Exception("El vértice inicial no existe en el grafo.")

    # Inicializar estructura de búsqueda
    visited_map = mp.new_map(G.order(graph))
    queue = q.new_queue()

    mp.put(visited_map, source, {"marked": True, "previous": None})
    q.enqueue(queue, source)

    while not q.is_empty(queue):
        vertex = q.dequeue(queue)
        bfs_vertex(vertex, visited_map, queue, graph)

    return visited_map

def bfs_vertex(key, visited_map, queue, graph):
    adj = G.adjacents(graph, key)
    for neighbor in adj["elements"]:
        if not mp.contains(visited_map, neighbor):
            mp.put(visited_map, neighbor, {"marked": True, "previous": key})
            q.enqueue(queue, neighbor)

def has_path_to(key, visited_map):
    return mp.contains(visited_map, key)

def path_to(key, visited_map):
    if not has_path_to(key, visited_map):
        return None
    
    path = []
    current = key
    while current is not None:
        path.append(current)
        current = mp.get(visited_map, current)["previous"]
    
    path.reverse()
    return path
