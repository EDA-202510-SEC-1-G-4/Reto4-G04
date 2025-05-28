import time
import csv
import os
from DataStructures.Graph import digraph as G
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al
from DataStructures.Graph import edge as edg  
from DataStructures.Graph import bfs as bfs
from DataStructures.Graph import dfs as dfs
from DataStructures.Graph import dijsktra_search as dj
from DataStructures.Queue import queue as q
from DataStructures.Stack import stack as s
import math



csv.field_size_limit(2147483647)
data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'

def new_logic():
    """
    Crea el catálogo con las estructuras de datos iniciales
    """
    catalog = {
        'deliveries': al.new_list(),
        'graph': G.new_graph(100),
        'nodes': mp.new_map(1000), 
        'domiciliarios':al.new_list(), # Para almacenar nodos de ubicación
        'domiciliarios_ultimos_destinos': mp.new_map(100),
        'domiciliarios_ultimos_tiempos': mp.new_map(100),
        'restaurant_locations': al.new_list(),
        'delivery_locations': al.new_list(),
        'total_delivery_time': 0.0,
        'total_deliveries': 0,
        'total_edges': 0,
        'load_time': 0.0
    }
    return catalog


# Funciones para la carga de datos


def format_location(lat, lon):
    """
    Formatea una coordenada (latitud o longitud) a 4 decimales
    """
    try:
        lat_f = "{0:.4f}".format(float(lat))
        lon_f = "{0:.4f}".format(float(lon))
        return f"{lat_f}_{lon_f}"
    except:
        return "0.0000_0.0000"

def list_contains(lst, value):
    """
    Verifica si un valor está en una lista (array_list)
    """
    for element in lst['elements']:
        if element == value:
            return True
    return False

def load_data(catalog, filename):
    start_time = get_time()
    file_path = os.path.join(data_dir, filename)

    csvfile = open(file_path, 'r', encoding='utf-8')
    reader = csv.DictReader(csvfile)

    for row in reader:
        origin = format_location(row['Restaurant_latitude'], row['Restaurant_longitude'])
        destination = format_location(row['Delivery_location_latitude'], row['Delivery_location_longitude'])
        time_taken = float(row['Time_taken(min)'])
        person_id = row['Delivery_person_ID']

        # Asegurar que los nodos existen
        if not G.contains_vertex(catalog['graph'], origin):
            doms = al.new_list()
            al.add_last(doms,person_id)
            catalog['graph'] = G.insert_vertex(catalog['graph'], origin, doms)
        else:
            node_doms = G.get_vertex_information(catalog['graph'],origin)
            al.add_last(node_doms,person_id)

        if not G.contains_vertex(catalog['graph'], destination):
            doms = al.new_list()
            al.add_last(doms,person_id)
            catalog['graph'] = G.insert_vertex(catalog['graph'], destination, doms)
        else:
            node_doms = G.get_vertex_information(catalog['graph'],destination)
            al.add_last(node_doms,person_id)

        # Crear entrega
        delivery = {
            'delivery_id': row['ID'],
            'person_id': person_id,
            'person_age': row.get('Delivery_person_Age', 'Unknown'),
            'person_rating': row.get('Delivery_person_Ratings', 'Unknown'),
            'origin': origin,
            'destination': destination,
            'order_type': row.get('Type_of_order', 'Unknown'),
            'vehicle_type': row.get('Type_of_vehicle', 'Unknown'),
            'time_taken': time_taken
        }

        al.add_last(catalog['deliveries'], delivery)
        catalog['total_delivery_time'] += time_taken
        catalog['total_deliveries'] += 1

        # Agregar domiciliario único
        if not al.contains(catalog['domiciliarios'],person_id):
            al.add_last(catalog['domiciliarios'], person_id)

        # Agregar domiciliarios a nodos
        for point in (origin, destination):
            node = mp.get(catalog['nodes'], point)
            if node is None:
                node = {'location': point, 'domiciliarios': al.new_list()}
                mp.put(catalog['nodes'], point, node)
            if not list_contains(node['domiciliarios'], person_id):
                al.add_last(node['domiciliarios'], person_id)

        # Ubicaciones únicas
        if not list_contains(catalog['restaurant_locations'], origin):
            al.add_last(catalog['restaurant_locations'], origin)
        if not list_contains(catalog['delivery_locations'], destination):
            al.add_last(catalog['delivery_locations'], destination)

        # Arcos principales (origen <-> destino)
        edge = G.get_edge(catalog['graph'], origin, destination)
        avg = time_taken
        if edge != None:
            avg = (edge['weight'] + time_taken)/2
        else:
            catalog['total_edges'] += 1
        catalog['graph'] = G.add_edge(catalog['graph'], origin, destination, avg)
        catalog['graph'] = G.add_edge(catalog['graph'], destination, origin, avg)

        # Conexión entre entregas consecutivas del mismo domiciliario
        prev_dest = mp.get(catalog['domiciliarios_ultimos_destinos'], person_id)
        prev_time = mp.get(catalog['domiciliarios_ultimos_tiempos'], person_id)
        if prev_dest and prev_dest != destination:
            avg_time = (prev_time + time_taken) / 2
            existing = G.get_edge(catalog['graph'], prev_dest, destination)
            if existing is None:
                catalog['graph'] = G.add_edge(catalog['graph'], prev_dest, destination, avg_time)
                catalog['graph'] = G.add_edge(catalog['graph'], destination, prev_dest, avg_time)
            else:
                final_avg = (existing['weight'] + avg_time) / 2
                catalog['graph'] = G.add_edge(catalog['graph'], prev_dest, destination, final_avg)
                catalog['graph'] = G.add_edge(catalog['graph'], destination, prev_dest, final_avg)

        # Actualizar info del domiciliario
        mp.put(catalog['domiciliarios_ultimos_destinos'], person_id, destination)
        mp.put(catalog['domiciliarios_ultimos_tiempos'], person_id, time_taken)

    csvfile.close()

    end_time = get_time()
    catalog['load_time'] = delta_time(start_time, end_time)
    catalog['total_unique_delivery_persons'] = al.size(catalog['domiciliarios'])  # Cantidad única de domiciliarios
    catalog['total_nodes'] = G.order(catalog['graph'])
    catalog['avg_delivery_time'] = catalog['total_delivery_time'] / catalog['total_deliveries']
    catalog['total_restaurants'] = al.size(catalog['restaurant_locations'])
    catalog['total_delivery_locations'] = al.size(catalog['delivery_locations'])
    catalog['total_edges'] = catalog['total_edges']

    return catalog


    
# Funciones de consulta sobre el catálogo

def get_data(catalog, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Consulta en las Llamar la función del modelo para obtener un dato
    pass


def req_1(catalog, point_a, point_b):
    
    start = get_time()

    if not G.contains_vertex(catalog['graph'], point_a) or not G.contains_vertex(catalog['graph'], point_b):
        end = get_time()
        return {
            'execution_time': delta_time(start, end),
            'points_count': 0,
            'path': [],
            'domiciliarios': [],
            'restaurants': [],
            'message': f'No existe un camino entre {point_a} y {point_b}.'
        }

    # Ejecutar BFS para buscar el camino
    search = bfs.bfs(catalog["graph"], point_a)

    if not has_path_to(search, point_b):
        end = get_time()
        return {
            'execution_time': delta_time(start, end),
            'points_count': 0,
            'path': [],
            'domiciliarios': [],
            'restaurants': [],
            'message': f'No hay conexión entre {point_a} y {point_b}.'
        }

   
    path = path_to(search, point_b)
    domiciliarios = set()
    restaurants = set()

    for node in path:
        node_info = mp.get(catalog["nodes"], node)
        if node_info:
            domiciliarios.update(node_info["domiciliarios"])

        if list_contains(catalog["restaurant_locations"], node):
            restaurants.add(node)

    end = get_time()

    return {
        'execution_time': delta_time(start, end),
        'points_count': len(path),
        'path': path,
        'domiciliarios': list(domiciliarios),
        'restaurants': list(restaurants)
    }


#FUNCIONES PARA REQ 1:

def has_path_to(search, vertex):
    return mp.contains(search['visited'], vertex)

def path_to(search, vertex):
    if not has_path_to(search, vertex):
        return None

    path = []
    current = vertex

    while current != search["source"]:
        path.append(current)
        current = mp.get(search['edge_to'], current)

    path.append(search["source"])
    path.reverse()  # Para que el camino quede en orden desde el origen hasta el destino

    return path
    


def error_response(start_time, error_message):
    """
    Crea una respuesta estandarizada para errores
    
    Args:
        start_time: Tiempo de inicio de la ejecución (para calcular duración)
        error_message: Mensaje descriptivo del error
    
    Returns:
        Un diccionario con la estructura estándar de respuesta pero indicando error
    """
    return {
        'execution_time': delta_time(start_time, get_time()),
        'path_length': 0,
        'path': [],
        'delivery_persons': [],
        'restaurants': [],
        'message': error_message
    }   
def req_2(catalog, point_a, point_b, delivery_person_id):
    """
    Implementa el requerimiento 2: Camino con menos puntos intermedios para un domiciliario específico
    """
    start_time = get_time()
    
    # Verificar que los puntos existen en el grafo principal
    if not G.contains_vertex(catalog['graph'], point_a):
        return error_response(start_time, f"El punto de origen {point_a} no existe")
        
    if not G.contains_vertex(catalog['graph'], point_b):
        return error_response(start_time, f"El punto de destino {point_b} no existe")
    
    # Verificar que el domiciliario existe
    if not any(delivery['person_id'] == delivery_person_id for delivery in catalog['deliveries']['elements']):
        return error_response(start_time, f"Domiciliario {delivery_person_id} no encontrado")

    # Crear grafo filtrado
    filtered_graph = create_filtered_graph(catalog, delivery_person_id)
    
    # Verificar que los puntos existen en el grafo filtrado
    if not G.contains_vertex(filtered_graph, point_a) or not G.contains_vertex(filtered_graph, point_b):
        return error_response(start_time, "No hay camino para este domiciliario entre las ubicaciones")

    # Ejecutar DFS en el grafo filtrado (diferente al req1 que usa BFS)
    search = dfs.dfs(filtered_graph, point_a)
    
    if not has_path_to(search, point_b):
        return error_response(start_time, "No existe camino para este domiciliario")

    # Obtener el camino
    path = path_to(search, point_b)
    
    # Procesar restaurantes en el camino
    restaurants = []
    for node in path:
        # Verificar si es restaurante buscando en restaurant_locations
        if node in catalog['restaurant_locations']['elements']:  # Acceso correcto a la lista
            restaurants.append(node)
    
    # Eliminar duplicados manteniendo orden
    unique_restaurants = []
    seen = set()
    for rest in restaurants:
        if rest not in seen:
            unique_restaurants.append(rest)
            seen.add(rest)
    
    return {
        'execution_time': delta_time(start_time, get_time()),
        'path_length': len(path),
        'path': path,
        'delivery_persons': [delivery_person_id],
        'restaurants': unique_restaurants,
        'message': 'Éxito'
    }

def create_filtered_graph(catalog, delivery_person_id):
    """Crea un grafo solo con arcos usados por el domiciliario"""
    filtered_graph = G.new_graph()
    
    # Agregar todos los vértices primero
    all_vertices = G.vertices(catalog['graph'])['elements']  # Acceso correcto a la lista
    for vertex in all_vertices:
        G.insert_vertex(filtered_graph, vertex, None)
    
    # Agregar solo arcos usados por este domiciliario
    for delivery in catalog['deliveries']['elements']:  # Acceso correcto a la lista
        if delivery['person_id'] == delivery_person_id:
            origin = delivery['origin']
            dest = delivery['destination']
            time = delivery['time_taken']
            
            if G.contains_vertex(filtered_graph, origin) and G.contains_vertex(filtered_graph, dest):
                G.add_edge(filtered_graph, origin, dest, time)
                G.add_edge(filtered_graph, dest, origin, time)
    
    return filtered_graph

def create_subgraph_for_delivery_person(catalog, delivery_person_id):
    """
    Crea un subgrafo que solo contiene arcos utilizados por el domiciliario especificado
    """
    subgraph = G.new_graph()
    
    # Agregar todos los nodos primero
    vertices = G.vertices(catalog['graph'])
    for vertex in vertices['elements']:
        G.insert_vertex(subgraph, vertex, None)
    
    # Agregar solo arcos utilizados por este domiciliario
    for delivery in catalog['deliveries']['elements']:
        if delivery['person_id'] == delivery_person_id:
            origin = delivery['origin']
            destination = delivery['destination']
            time_taken = delivery['time_taken']
            
            # Agregar arco en ambas direcciones (grafo no dirigido)
            if not G.contains_vertex(subgraph, origin):
                G.insert_vertex(subgraph, origin, None)
            if not G.contains_vertex(subgraph, destination):
                G.insert_vertex(subgraph, destination, None)
                
            existing_edge = G.get_edge(subgraph, origin, destination)
            if existing_edge is None:
                G.add_edge(subgraph, origin, destination, time_taken)
                G.add_edge(subgraph, destination, origin, time_taken)
    
    return subgraph

def is_restaurant(catalog, node_id):
    """
    Verifica si un nodo es un restaurante buscando en la lista de ubicaciones de restaurantes
    
    Args:
        catalog: El catálogo con los datos cargados
        node_id: ID del nodo a verificar (formato "lat_lon")
    
    Returns:
        True si el nodo es un restaurante, False en caso contrario
    """
    # Convertir el array_list a lista normal para búsqueda más eficiente
    restaurant_locations = catalog['restaurant_locations']['elements']
    return node_id in restaurant_locations



def req_3(catalog, point_a):
    start = get_time()

    if not G.contains_vertex(catalog['graph'], point_a):
        end = get_time()
        return {
            'execution_time': delta_time(start, end),
            'domiciliary_id': None,
            'total_deliveries': 0,
            'most_used_vehicle': None,
            'message': f'La ubicación {point_a} no existe en el grafo.'
        }

    counts = mp.new_map(100)
    
    for delivery in catalog['deliveries']['elements']:
        if delivery['origin'] == point_a or delivery['destination'] == point_a:
            person = delivery['person_id']
            vehicle = delivery['vehicle_type']

            person_entry = mp.get(counts, person)
            if person_entry is None:
                person_entry = {
                    'count': 1,
                    'vehicles': mp.new_map(5)
                }
                mp.put(person_entry['vehicles'], vehicle, 1)
                mp.put(counts, person, person_entry)
            else:
                person_entry['count'] += 1
                veh_count = mp.get(person_entry['vehicles'], vehicle)
                if veh_count is None:
                    mp.put(person_entry['vehicles'], vehicle, 1)
                else:
                    mp.put(person_entry['vehicles'], vehicle, veh_count + 1)

    # Buscar el domiciliario con más entregas
    max_person = None
    max_count = 0
    max_vehicle = None

    for entry in counts['table']['elements']:
        if entry and entry['key'] is not None:
            person = entry['key']
            info = entry['value']
            if info['count'] > max_count:
                max_count = info['count']
                max_person = person
                # Buscar vehículo más usado
                max_vehicle_count = 0
                for v_entry in info['vehicles']['table']['elements']:
                    if v_entry and v_entry['key'] is not None:
                        if v_entry['value'] > max_vehicle_count:
                            max_vehicle_count = v_entry['value']
                            max_vehicle = v_entry['key']

    end = get_time()

    return {
        'execution_time': delta_time(start, end),
        'domiciliary_id': max_person,
        'total_deliveries': max_count,
        'most_used_vehicle': max_vehicle
    }


def req_4(catalog, point_a, point_b):
    start = get_time()

    if not G.contains_vertex(catalog['graph'], point_a) or not G.contains_vertex(catalog['graph'], point_b):
        return {
            'execution_time': delta_time(start, get_time()),
            'path': [],
            'common_domiciliaries': al.new_list(),
            'message': 'Uno o ambos puntos no existen en el grafo.'
        }

    search = bfs.bfs(catalog['graph'], point_a)
    if not has_path_to(search, point_b):
        return {
            'execution_time': delta_time(start, get_time()),
            'path': [],
            'common_domiciliaries': al.new_list(),
            'message': 'No hay camino entre los dos puntos.'
        }

    path = path_to(search, point_b)

    # Obtener domiciliarios desde catalog['nodes']
    domis_a = mp.get(catalog["nodes"], point_a)
    domis_b = mp.get(catalog["nodes"], point_b)

    if domis_a is None or domis_b is None:
        return {
            'execution_time': delta_time(start, get_time()),
            'path': path,
            'common_domiciliaries': al.new_list(),
            'message': 'No se encontraron domiciliarios en uno o ambos puntos.'
        }

    # Crear mapas para facilitar búsqueda
    candidatos = mp.new_map(50)
    for d in domis_a["domiciliarios"]["elements"]:
        d_id = d.strip()
        if al.contains(domis_b["domiciliarios"], d_id):
            mp.put(candidatos, d_id, True)

    # Revisar domiciliarios que recorren todo el camino
    domis_en_camino = mp.new_map(100)
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        nodo_u = mp.get(catalog["nodes"], u)
        nodo_v = mp.get(catalog["nodes"], v)

        if nodo_u is None or nodo_v is None:
            continue

        for d in nodo_u["domiciliarios"]["elements"]:
            if al.contains(nodo_v["domiciliarios"], d):
                mp.put(domis_en_camino, d.strip(), True)

    # Intersección final
    domis_comunes = al.new_list()
    for pair in candidatos["table"]["elements"]:
        if pair and pair['key'] is not None:
            if mp.contains(domis_en_camino, pair['key']):
                al.add_last(domis_comunes, pair['key'])

    end = get_time()
    
  
    return {
        'execution_time': delta_time(start, end),
        'path': path,
        'common_domiciliaries': domis_comunes,
        'message': 'Camino encontrado exitosamente.'
    }

def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia geográfica entre dos puntos usando la fórmula de Haversine.
    Retorna la distancia en kilómetros.
    """
    R = 6371  # Radio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c




def req_5(catalog, point_a, n_changes):
    start_time = get_time()

    # Verificar si el punto de inicio existe en el grafo
    if not G.contains_vertex(catalog['graph'], point_a):
        end_time = get_time()
        return {
            'execution_time': delta_time(start_time, end_time),
            'domiciliary_id': None,
            'max_distance_km': 0,
            'path': [],
            'message': f'El punto {point_a} no existe en el grafo.'
        }

    # Ejecutar BFS para encontrar rutas desde el punto A
    search = bfs.bfs(catalog["graph"], point_a)

    # Almacenar la distancia recorrida por cada domiciliario
    domiciliarios_distancias = mp.new_map(100)
    path_distances = {}

    for delivery in catalog['deliveries']['elements']:
        # Usar directamente 'origin' y 'destination'
        origin = delivery['origin']
        destination = delivery['destination']
        person_id = delivery['person_id']

        if "_" in origin and "_" in destination:
            lat1, lon1 = map(float, origin.split('_'))
            lat2, lon2 = map(float, destination.split('_'))
            dist = haversine(lat1, lon1, lat2, lon2)
        else:
            print(f"⚠️ Datos inválidos -> origin: {origin}, destination: {destination}")
            dist = 0  # Evita errores si los datos no tienen el formato esperado

        # Registrar distancia recorrida por cada domiciliario
        if mp.contains(domiciliarios_distancias, person_id):
            prev_dist = mp.get(domiciliarios_distancias, person_id)
            mp.put(domiciliarios_distancias, person_id, prev_dist + dist)
        else:
            mp.put(domiciliarios_distancias, person_id, dist)

        # Registrar los caminos posibles
        path_distances[person_id] = path_to(search, person_id)

    # Encontrar el domiciliario con mayor distancia recorrida en N cambios
    max_person = None
    max_distance = 0
    max_path = []

    for pair in domiciliarios_distancias['table']['elements']:
        if pair and pair['key'] is not None:
            person_id = pair['key']
            total_distance = pair['value']
            path = path_distances.get(person_id, [])[:n_changes]  # Tomar solo los primeros N cambios

            if total_distance > max_distance:
                max_distance = total_distance
                max_person = person_id
                max_path = path

    end_time = get_time()

    return {
        'execution_time': delta_time(start_time, end_time),
        'domiciliary_id': max_person,
        'max_distance_km': max_distance,
        'path': max_path,
        'message': 'Análisis completado exitosamente.'
    }

import time

def req_6(catalog, start):
    graph = catalog['graph']
    start_time = time.time()  # ⏳ Iniciar medición del tiempo

    # 1. Ejecutar Dijkstra en el grafo desde la ubicación inicial
    search = dj.dijkstra(graph, start)

    if search is None:
        return {"message": "No hay caminos disponibles desde la ubicación dada."}

    # 2. Extraer ubicaciones alcanzables y ordenarlas alfabéticamente
    reachable_locations = al.new_list()
    for location in mp.key_set(search["dist_to"])["elements"]:
        if has_path_to(search,location):  # Solo considerar ubicaciones alcanzables
            al.add_last(reachable_locations, location)

    sorted_locations = al.merge_sort(reachable_locations, al.default_sort_criteria)  # Ordenar ubicaciones

    # 3. Identificar el camino de mayor tiempo desde 'start'
    longest_path = None
    max_time = float('-inf')
    
    for location in sorted_locations["elements"]:
        time_cost = dj.dist_to(location, search)
        if time_cost > max_time:
            max_time = time_cost
            longest_path = path_to(search, location)  # Ahora se obtiene como lista directamente

    end_time = time.time()  # ⏳ Finalizar medición del tiempo
    execution_time = round(end_time - start_time, 4)
    total_locations = al.size(sorted_locations)

    return execution_time,total_locations,sorted_locations['elements'],longest_path,max_time

    # 4. Retornar información en el formato esperado
    # return {
    #     "execution_time": execution_time,
    #     "total_locations": al.size(sorted_locations),
    #     "reachable_locations": sorted_locations["elements"],
    #     "longest_path": longest_path,  # `longest_path` ya es una lista ordenada
    #     "longest_path_time": max_time
    # }


def req_7(catalog):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass


def req_8(catalog):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
