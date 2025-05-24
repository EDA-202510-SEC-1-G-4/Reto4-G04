from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Queue import queue as q
from DataStructures.Stack import stack as s
from DataStructures.Graph import digraph as G

def dfs(my_graph, source):
    """
    Inicia el recorrido DFS desde el vértice source.
    Retorna la estructura de búsqueda DFS con visited y edge_to.
    """
    visited = mp.new_map(100)

    mp.put(visited, source, {
        "marked": True,
        "edge_to": None
    })

    search = {
        'source': source,
        'visited': visited
    }

    dfs_vertex(my_graph, source, search)
    return search

def dfs_vertex(my_graph, vertex, search):
    """
    Recorre el grafo desde vertex de forma recursiva usando DFS.
    Marca cada vértice y guarda su predecesor (edge_to).
    """
    visited = search['visited']

    entry = mp.get(my_graph['vertices'], vertex)
    if entry is None:
        raise Exception(f"Vértice '{vertex}' no encontrado en el grafo.")

    adj_map = entry["adjacents"]
    adj_keys = mp.key_set(adj_map)

    for key in adj_keys["elements"]:
        if not mp.contains(visited, key):
            mp.put(visited, key, {
                "marked": True,
                "edge_to": vertex
            })
            dfs_vertex(my_graph, key, search)

def has_path_to(search, vertex):
    """
    Retorna True si hay camino desde search['source'] hasta vertex.
    """
    return mp.contains(search['visited'], vertex)

def path_to(search, vertex):
    """
    Retorna una pila con el camino desde source hasta vertex.
    Si no existe camino, retorna None.
    """
    if not has_path_to(search, vertex):
        return None

    path = s.new_stack()
    current = vertex

    while current != search['source']:
        s.push(path, current)
        current = mp.get(search['visited'], current)['edge_to']

    s.push(path, search['source'])
    return path
