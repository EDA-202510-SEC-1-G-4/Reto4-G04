import time
import csv
import os
from DataStructures.Graph import digraph as G
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al
from DataStructures.Graph import edge as edg  

csv.field_size_limit(2147483647)
data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'

def new_logic():
    """
    Crea el catálogo con las estructuras de datos iniciales
    """
    catalog = {
        'graph': G.new_graph(),
        'delivery_persons': mp.new_map(100),
        'deliveries_count': 0,
        'last_delivery': mp.new_map(100),
        'restaurants': mp.new_map(100),
        'delivery_locations': mp.new_map(100),
        'delivery_person_set': set(),
        'total_delivery_time': 0.0
    }
    return catalog


# Funciones para la carga de datos
def format_coordinate(coord):
    """Formatea coordenadas a exactamente 4 decimales"""
    return "{0:.4f}".format(float(coord))

def create_node_id(lat, lon):
    """Crea ID de nodo en formato 'latitud_longitud' con 4 decimales"""
    return f"{format_coordinate(lat)}_{format_coordinate(lon)}"


def load_data(catalog, filename):
    """
    Carga datos de domicilios desde archivo CSV y construye el grafo
    Devuelve diccionario con estadísticas de carga
    """
    start_time = time.time()

    filename = data_dir + filename
    csvfile = open(filename,'r',encoding='utf-8')
    reader = csv.DictReader(csvfile)
        
    for row in reader:
            # Procesamiento básico de cada registro
        catalog['deliveries_count'] += 1
        delivery_person_id = row['Delivery_person_ID']
            
            # Registro de domiciliarios únicos
        catalog['delivery_person_set'].add(delivery_person_id)
            
            # Creación de IDs de nodos
        origin_id = create_node_id(row['Restaurant_latitude'], row['Restaurant_longitude'])
        dest_id = create_node_id(row['Delivery_location_latitude'], row['Delivery_location_longitude'])
            
            # Acumulación de tiempo total
        time_taken = float(row['Time_taken(min)'])
        catalog['total_delivery_time'] += time_taken
            
            # Registro de ubicaciones únicas
        if not mp.contains(catalog['restaurants'], origin_id):
            mp.put(catalog['restaurants'], origin_id, True)
            
        if not mp.contains(catalog['delivery_locations'], dest_id):
            mp.put(catalog['delivery_locations'], dest_id, True)
            
            # Creación de nodos si no existen
        if not G.contains_vertex(catalog['graph'], origin_id):
            G.insert_vertex(catalog['graph'], origin_id, {
                'type': 'restaurant',
                'delivery_persons': set()})
            
        if not G.contains_vertex(catalog['graph'], dest_id):
            G.insert_vertex(catalog['graph'], dest_id, {
                'type': 'delivery_location',
                'delivery_persons': set()})
            
            # Obtención de vértices
        origin_vertex = G.get_vertex(catalog['graph'], origin_id)
        dest_vertex = G.get_vertex(catalog['graph'], dest_id)
            
            # Asociación de domiciliarios a nodos
        origin_vertex['value']['delivery_persons'].add(delivery_person_id)
        dest_vertex['value']['delivery_persons'].add(delivery_person_id)
            
            # Manejo de arcos entre origen y destino
        existing_edge = G.get_edge(catalog['graph'], origin_id, dest_id)
        if existing_edge:
                # Actualización de peso existente (promedio)
            new_weight = (existing_edge['weight'] + time_taken) / 2
            G.add_edge(catalog['graph'], origin_id, dest_id, new_weight)
            G.add_edge(catalog['graph'], dest_id, origin_id, new_weight)
        else:
                # Creación de nuevos arcos
            G.add_edge(catalog['graph'], origin_id, dest_id, time_taken)
            G.add_edge(catalog['graph'], dest_id, origin_id, time_taken)
            
            # Conexión con último destino del mismo domiciliario
        if mp.contains(catalog['last_delivery'], delivery_person_id):
            last_dest_id = mp.get(catalog['last_delivery'], delivery_person_id)
                
            if last_dest_id != dest_id:
                    # Manejo de arcos entre destinos consecutivos
                existing_connection = G.get_edge(catalog['graph'], dest_id, last_dest_id)
                if existing_connection:
                    new_conn_weight = (existing_connection['weight'] + time_taken) / 2
                    G.add_edge(catalog['graph'], dest_id, last_dest_id, new_conn_weight)
                    G.add_edge(catalog['graph'], last_dest_id, dest_id, new_conn_weight)
                else:
                    G.add_edge(catalog['graph'], dest_id, last_dest_id, time_taken)
                    G.add_edge(catalog['graph'], last_dest_id, dest_id, time_taken)
            
            # Actualización del último destino
        mp.put(catalog['last_delivery'], delivery_person_id, dest_id)
    
    # Cálculo de estadísticas finales
    execution_time = time.time() - start_time
    avg_time = catalog['total_delivery_time'] / catalog['deliveries_count'] if catalog['deliveries_count'] > 0 else 0
    
    return {
        'total_deliveries': catalog['deliveries_count'],
        'total_delivery_persons': len(catalog['delivery_person_set']),
        'total_nodes': G.order(catalog['graph']),
        'total_edges': G.size(catalog['graph']) // 2,
        'total_restaurants': mp.size(catalog['restaurants']),
        'total_delivery_locations': mp.size(catalog['delivery_locations']),
        'avg_delivery_time': avg_time,
        'execution_time': execution_time
    }
    
# Funciones de consulta sobre el catálogo

def get_data(catalog, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Consulta en las Llamar la función del modelo para obtener un dato
    pass


def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


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
