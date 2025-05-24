from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Stack import stack as s
from DataStructures.Graph import digraph as G

def dfo(graph):
    # Inicializar estructura de búsqueda para el recorrido DFO
    dfo_search = mp.new_map(G.order(graph))  
    stack = s.new_stack()

    # Obtener todos los vértices del grafo
    vertices_list = G.vertices(graph)['elements']

    for vertex in vertices_list:
        if not mp.contains(dfo_search, vertex):
            dfs_vertex(graph, vertex, dfo_search, stack)  

    return dfo_search

def dfs_vertex(graph, key, dfo_search, stack):
    # Registrar el nodo como visitado
    mp.put(dfo_search, key, {"marked": True})
    s.push(stack, key)

    adj = G.adjacents(graph, key)["elements"]
    for neighbor in adj:
        if not mp.contains(dfo_search, neighbor):
            dfs_vertex(graph, neighbor, dfo_search, stack)

    s.pop(stack)