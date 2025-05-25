from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Queue import queue as q
from DataStructures.Stack import stack as s
from DataStructures.Graph import digraph as G
from DataStructures.Graph import dfo_structure as dfos

def dfo(my_graph):
    """
    Inicia un recorrido Depth First Order (DFO) sobre el grafo.
    Retorna una estructura de búsqueda para determinar el orden de los vértices.
    """
    order = G.order(my_graph)
    search = dfos.new_dfo_structure(order)
    vertices = G.vertices(my_graph)  # array_list

    for v in vertices["elements"]:
        if not mp.contains(search['marked'], v):
            dfs_vertex(my_graph, v, search)

    return search

def dfs_vertex(my_graph, vertex, search):
    """
    Función recursiva que aplica DFS actualizando pre, post y reversepost.
    """
    q.enqueue(search['pre'], vertex)
    mp.put(search['marked'], vertex, True)

    entry = mp.get(my_graph['vertices'], vertex)
    adj_map = entry['adjacents']
    adj_keys = mp.key_set(adj_map)

    for adj in adj_keys["elements"]:
        if not mp.contains(search['marked'], adj):
            dfs_vertex(my_graph, adj, search)

    q.enqueue(search['post'], vertex)
    s.push(search['reversepost'], vertex)

    return search
