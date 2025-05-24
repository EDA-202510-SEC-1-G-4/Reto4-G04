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
    edge_to = mp.new_map(100)

    search = {
        'source': source,
        'visited': visited,
        'edgeTo': edge_to
    }

    bfs_vertex(my_graph, source, search)
    return search




def bfs_vertex(my_graph, source, search):
    """
    Función auxiliar que realiza el recorrido BFS.
    Llena los mapas de visitados y predecesores.
    """
    visited = search['visited']
    edge_to = search['edgeTo']
    queue = q.new_queue()

    mp.put(visited, source, True)
    q.enqueue(queue, source)

    while not q.is_empty(queue):
        current = q.dequeue(queue)
        entry = mp.get(my_graph['vertices'], current)
        if entry is None:
            raise Exception(f"Vértice '{current}' no encontrado en el grafo.")
        print(entry)
        vertex = entry['value']
        print(vertex)
        print(entry["adjacents"])
        adj_keys = mp.key_set(entry["adjacents"])

        for i in range(mp.size(adj_keys)):
            adj = mp.get(adj_keys, i)['value']
            if not mp.contains(visited, adj):
                mp.put(visited, adj, True)
                mp.put(edge_to, adj, current)
                q.enqueue(queue, adj)

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
        current = mp.get(search['edgeTo'], current)['value']

    s.push(path, search['source'])
    return path


