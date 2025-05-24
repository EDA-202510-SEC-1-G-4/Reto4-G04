from DataStructures.Graph import edge
from DataStructures.Graph import vertex
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al

def new_graph(order):
    graph = {'vertices':mp.new_map(order),
             'num_edges':0}
    return graph

def insert_vertex(graph,key,info):
    if key != None and graph != None:
        nodo = vertex.new_vertex(key,info)
        graph['vertices'] = mp.put(graph['vertices'],key,nodo)
    return graph

def update_vertex_info(graph,key,info): #da.rincon
    vertices = graph["vertices"]
    vertice = mp.get(vertices,key)
    vertex.set_value(vertice,info)
    return graph
def remove_vertex(graph,key):
    if graph != None and key != None:
        info_eliminado = mp.get(graph['vertices'],key) 
        adj_elim = mp.key_set(info_eliminado['adjacents'])
        for adj in adj_elim:
            mp.remove(mp.get(graph['vertices'],adj)['adjacents'],key)
            graph['edges'] -= 1
        graph['vertices'] = mp.remove(graph['vertices'],key)
    return graph

def add_edge(graph, key_u, key_v, weight=1.0):#ncastano que hizo 
    
    if not mp.contains(graph['vertices'], key_u):
        raise Exception("El vertice no existe")
        
    if not mp.contains(graph['vertices'], key_v):
        raise Exception("El vertice no existe")

    existe = mp.contains(mp.get(graph['vertices'], key_u)['adjacents'], key_v)
    e = edge.new_edge(key_v, weight)
    
    mp.put(mp.get(graph['vertices'], key_u)['adjacents'], key_v, e)
    
    if not existe:
        graph['num_edges'] += 1
    
    return graph

def order(graph): #tranca
    vertices = mp.size(graph['vertices'])
    return vertices

def size(graph):
    return graph['num_edges']

def vertices(graph):
    vertices = graph["vertices"]
    retorno = mp.key_set(vertices)
    return retorno

def degree(graph,key_u):
    if not mp.contains(graph["vertices"],key_u):
        raise Exception("El vertice no existe")
    else:
        vertice = mp.get(graph["vertices"],key_u)
        retorno = mp.size(vertice["adjacents"])
    return retorno

def get_edge(graph, key_u, key_v):
    if key_u not in graph['vertices']:
        raise Exception("El vertice u no existe")
    
    vertex_u = graph['vertices'][key_u]
    
    for edge in vertex_u['out_edges']:
        if edge['target'] == key_v:
            return edge
    
    return None

def get_vertex_information(graph, key_u):
    vertex = mp.get(graph["vertices"], key_u)
    
    if vertex is None:
        raise Exception("El vertice no existe")
    
    return vertex["value"]

def contains_vertex(graph,key):
    vertices = graph['vertices']  
    existe = False
    nodo = mp.get(vertices,key)
    if nodo != None:
        existe = True
    return existe

def adjacents(graph,key):
    vertices = graph['vertices']
    nodo = mp.get(vertices,key)
    adj = al.new_list()
    if nodo == None:
        raise Exception("El vertice no existe.")
    else:
        adj = mp.key_set(nodo['adjacents'])
    return adj

def edges_vertex(graph,key_u):
    vertex = mp.get(graph["vertices"], key_u)
    if vertex is None:
        raise Exception("El vertice no existe")
    
    adjacents_map = mp.value_set(vertex["adjacents"])
    return adjacents_map

def get_vertex(graph,key):
    vertices = graph['vertices']
    node = mp.get(vertices,key)
    if node == None:
        raise Exception("El vertice no existe.")
    return node
