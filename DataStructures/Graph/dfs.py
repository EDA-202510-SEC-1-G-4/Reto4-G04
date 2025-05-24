from DataStructures.List import array_list as al
from DataStructures.Stack import stack as s
from DataStructures.Graph import digraph as G
from DataStructures.Map import map_linear_probing as mp
'''''
def dfs(grafo,source):
    visited = al.new_list()
    stack = s.new_stack()
    s.push(stack,source)
    while s.size(stack) > 0:
        elem = s.pop(stack)
        if elem not in visited['elements']:
            al.add_last(visited,elem)
            for nodo in G.adjacents(grafo,elem)['elements']:
                if nodo not in visited['elements']:
                    s.push(stack,nodo)
    return visited
    '''''
def dfs(graph, source):
    if not G.contains_vertex(graph, source):
        raise Exception(f"El vértice '{source}' no existe en el grafo.")

    visited = mp.new_map(10)
    pre = al.new_list()
    post = al.new_list()
    reversepost = al.new_list()

    mp.put(visited, source, {'marked': True, 'edge_from': None})
    dfs_vertex(graph, source, visited, pre, post, reversepost)

    return {
        'source': source,
        'visited': visited,
        'pre': pre,
        'post': post,
        'reversepost': reversepost
    }

def dfs_vertex(graph, vertex_key, visited, pre, post, reversepost):
    al.add_last(pre, vertex_key)

    if not G.contains_vertex(graph, vertex_key):
        if not vertex_key == "elements":
            
            raise Exception(f"Vértice '{vertex_key}' no encontrado al intentar obtener adyacentes.")

    for neighbor in G.adjacents(graph, vertex_key):
        if not mp.contains(visited, neighbor):
            mp.put(visited, neighbor, {'marked': True, 'edge_from': vertex_key})
            dfs_vertex(graph, neighbor, visited, pre, post, reversepost)

    al.add_last(post, vertex_key)
    al.add_first(reversepost, vertex_key)

def has_path_to(vertex_key, search):
    """
    Retorna True si hay un camino desde el vértice fuente a vertex_key.
    """
    return mp.contains(search['visited'], vertex_key)

def path_to(search, vertex_key):
    """
    Reconstruye el camino desde el vértice fuente hasta vertex_key.
    """
    if not has_path_to(vertex_key, search):
        return None

    path = []
    current = vertex_key
    while current != search['source']:
        path.insert(0, current)
        current = mp.get(search['visited'], current)['edge_from']
    
    path.insert(0, search['source'])
    return path


