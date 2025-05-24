from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Queue import queue as q
from DataStructures.Stack import stack as s
from DataStructures.Graph import digraph as G

def bfs(my_graph, source):
    """
    Inicia el recorrido BFS desde el vértice source.
    Retorna la estructura de búsqueda graph_search.
    """
    visited = mp.new_map(100)

    mp.put(visited, source, {
        "marked": True,
        "edge_to": None,
        "dist_to": 0
    })

    search = {
        'source': source,
        'visited': visited
    }

    bfs_vertex(my_graph, search)
    return search

def bfs_vertex(my_graph, search):
    """
    Función auxiliar que realiza el recorrido BFS.
    Llena los mapas de visitados y predecesores.
    """
    visited = search['visited']
    queue = q.new_queue()

    q.enqueue(queue, search['source'])

    while not q.is_empty(queue):
        current = q.dequeue(queue)
        entry = mp.get(my_graph['vertices'], current)
        if entry is None:
            raise Exception(f"Vértice '{current}' no encontrado en el grafo.")

        current_dist = mp.get(visited, current)['dist_to']
        adj_map = entry["adjacents"]
        adj_keys = mp.key_set(adj_map)
        print(adj_keys)
        print(adj_map)
        print()
        for key in adj_keys["elements"]:
            adj = mp.get(adj_map, key)
            print(f"adyacente: {adj}")
            print(mp.contains(visited, adj))
            if not mp.contains(visited, adj):
                mp.put(visited, adj, {
                    "marked": True,
                    "edge_to": current,
                    "dist_to": current_dist + 1
                })
                q.enqueue(queue, adj)
            print()
            print(visited)

def has_path_to(vertex, search):
    """
    Retorna True si hay camino desde search['source'] hasta vertex.
    """
    return mp.contains(search['visited'], vertex)

def path_to(vertex, search):
    """
    Retorna una pila con el camino desde source hasta vertex.
    Si no existe camino, retorna None.
    """
    if not has_path_to(vertex, search):
        return None

    path = s.new_stack()
    current = vertex

    while current != search['source']:
        s.push(path, current)
        current = mp.get(search['visited'], current)['value']['edge_to']

    s.push(path, search['source'])
    return path
