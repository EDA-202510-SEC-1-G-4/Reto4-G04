from DataStructures.Map import map_linear_probing as mp
from DataStructures.Priority_queue import priority_queue as pq


def new_dijsktra_structure(source, g_order):
    """

    Crea una estructura de busqueda usada en el algoritmo **dijsktra**.

    Se crea una estructura de busqueda con los siguientes atributos:

    - **source**: Vertice de origen. Se inicializa en ``source``
    - **visited**: Mapa con los vertices visitados. Se inicializa en ``None``
    - **pq**: Cola indexada con los vertices visitados. Se inicializa en ``None``

    :returns: Estructura de busqueda
    :rtype: dijsktra_search
    """
    structure = {
        "source": source,
        "visited": mp.new_map(
            g_order, 0.5),
        "pq": pq.new_heap()}
    return structure

def dijkstra(grafo, source):
    distancias = {}
    caminos = {}
    visitados = []
    
    # Inicializar distancias y caminos
    for nodo in grafo:
        distancias[nodo] = float('inf')
        caminos[nodo] = []
    distancias[source] = 0
    caminos[source] = [source]
    
    # Cola simple (versión menos eficiente que PriorityQueue)
    cola = [source]
    
    while len(cola) > 0:
        # Encontrar nodo con menor distancia en la cola
        nodo_actual = None
        min_dist = float('inf')
        for nodo in cola:
            if distancias[nodo] < min_dist:
                min_dist = distancias[nodo]
                nodo_actual = nodo
        
        cola.remove(nodo_actual)
        visitados.append(nodo_actual)
        
        # Explorar vecinos
        vecinos = grafo[nodo_actual]
        for vecino in vecinos:
            peso = grafo[nodo_actual][vecino]
            nueva_distancia = distancias[nodo_actual] + peso
            
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                caminos[vecino] = caminos[nodo_actual] + [vecino]
                
                if vecino not in visitados and vecino not in cola:
                    cola.append(vecino)
    
    return distancias, caminos   
    


def dist_to(key_v, aux_structure):
    if not mp.contains(aux_structure['dist_to'], key_v):
        raise Exception("Vértice no encontrado en dist_to")
    return mp.get(aux_structure['dist_to'], key_v)

def has_path_to(key_v, aux_structure):
    return mp.get(aux_structure['dist_to'], key_v) < float('inf')

def path_to(key_v, aux_structure):
    if not has_path_to(key_v, aux_structure):
        raise Exception("No existe camino al vértice")
    
    path = []
    current = key_v
    
    while current is not None and current != aux_structure['source']:
        path.append(current)
        current = mp.get(aux_structure['edge_to'], current)
    
    path.append(aux_structure['source'])
    path.reverse()
    
    return path