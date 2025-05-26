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
        'delivery_person_set': mp.new_map(100),
        'total_delivery_time': 0.0
    }
    return catalog


# Funciones para la carga de datos


def format_location(lat, lon):
    """Formatea coordenadas a string con 4 decimales"""
    return f"{float(lat):.4f}_{float(lon):.4f}"

def load_data(catalog, filename):
    """
    Carga datos de domicilios desde archivo CSV y construye el grafo
    Versión sin usar dataclass, utilizando nuestras estructuras de datos propias
    """
    start_time = time.time()
    
    # Configuración de rutas
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Data")
    file_path = os.path.join(data_dir, filename)
    
    # Inicialización de estructuras si no existen
    if 'graph' not in catalog:
        catalog['graph'] = mp.new_map(100)  # Mapa para el grafo (origen -> destinos)
    if 'nodes' not in catalog:
        catalog['nodes'] = mp.new_map(100)  # Mapa para nodos (ubicación -> info)
    if 'last_delivery' not in catalog:
        catalog['last_delivery'] = mp.new_map(100)  # Mapa para últimos destinos por domiciliario
    if 'last_time' not in catalog:
        catalog['last_time'] = mp.new_map(100)  # Mapa para últimos tiempos por domiciliario
    if 'restaurants' not in catalog:
        catalog['restaurants'] = al.new_list()  # Lista de ubicaciones de restaurantes
    if 'delivery_locations' not in catalog:
        catalog['delivery_locations'] = al.new_list()  # Lista de ubicaciones de entrega
    if 'total_time' not in catalog:
        catalog['total_time'] = 0.0
    if 'total_deliveries' not in catalog:
        catalog['total_deliveries'] = 0
    if 'total_edges' not in catalog:
        catalog['total_edges'] = 0

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Procesamiento de cada fila
            origin = format_location(row['Restaurant_latitude'], row['Restaurant_longitude'])
            destination = format_location(row['Delivery_location_latitude'], row['Delivery_location_longitude'])
            time_taken = float(row['Time_taken(min)'])
            
            # Actualización de estadísticas
            catalog['total_time'] += time_taken
            catalog['total_deliveries'] += 1
            
            # Registro de ubicaciones únicas
            if not al.is_present(catalog['restaurants'], origin):
                al.add_last(catalog['restaurants'], origin)
                
            if not al.is_present(catalog['delivery_locations'], destination):
                al.add_last(catalog['delivery_locations'], destination)
            
            # Manejo de nodos
            if not mp.contains(catalog['nodes'], origin):
                node_info = {
                    'location': origin,
                    'delivery_persons': mp.new_map(10)
                }
                mp.put(catalog['nodes'], origin, node_info)
                
            if not mp.contains(catalog['nodes'], destination):
                node_info = {
                    'location': destination,
                    'delivery_persons': mp.new_map(10)
                }
                mp.put(catalog['nodes'], destination, node_info)
            
            # Asociar domiciliario con nodos
            origin_node = mp.get(catalog['nodes'], origin)
            dest_node = mp.get(catalog['nodes'], destination)
            delivery_person_id = row['Delivery_person_ID']
            
            if not mp.contains(origin_node['value']['delivery_persons'], delivery_person_id):
                mp.put(origin_node['value']['delivery_persons'], delivery_person_id, True)
                
            if not mp.contains(dest_node['value']['delivery_persons'], delivery_person_id):
                mp.put(dest_node['value']['delivery_persons'], delivery_person_id, True)
            
            # Manejo de arcos en el grafo
            if not mp.contains(catalog['graph'], origin):
                mp.put(catalog['graph'], origin, mp.new_map(10))
                
            if not mp.contains(catalog['graph'], destination):
                mp.put(catalog['graph'], destination, mp.new_map(10))
            
            origin_edges = mp.get(catalog['graph'], origin)
            dest_edges = mp.get(catalog['graph'], destination)
            
            # Conexión origen-destino (bidireccional)
            if not mp.contains(origin_edges['value'], destination):
                mp.put(origin_edges['value'], destination, time_taken)
                mp.put(dest_edges['value'], origin, time_taken)
                catalog['total_edges'] += 1
            else:
                current_time = mp.get(origin_edges['value'], destination)
                new_avg = (current_time + time_taken) / 2
                mp.put(origin_edges['value'], destination, new_avg)
                mp.put(dest_edges['value'], origin, new_avg)
            
            # Conexión con último destino del mismo domiciliario
            if mp.contains(catalog['last_delivery'], delivery_person_id):
                last_dest = mp.get(catalog['last_delivery'], delivery_person_id)
                last_time = mp.get(catalog['last_time'], delivery_person_id)
                
                if last_dest != destination:
                    # Manejo de arcos entre destinos consecutivos
                    if not mp.contains(catalog['graph'], last_dest):
                        mp.put(catalog['graph'], last_dest, mp.new_map(10))
                    
                    last_dest_edges = mp.get(catalog['graph'], last_dest)
                    avg_time = (last_time + time_taken) / 2
                    
                    if not mp.contains(last_dest_edges['value'], destination):
                        mp.put(last_dest_edges['value'], destination, avg_time)
                        mp.put(dest_edges['value'], last_dest, avg_time)
                    else:
                        current_avg = mp.get(last_dest_edges['value'], destination)
                        new_avg = (current_avg + avg_time) / 2
                        mp.put(last_dest_edges['value'], destination, new_avg)
                        mp.put(dest_edges['value'], last_dest, new_avg)
            
            # Actualizar último destino y tiempo
            mp.put(catalog['last_delivery'], delivery_person_id, destination)
            mp.put(catalog['last_time'], delivery_person_id, time_taken)
    
    # Cálculo de estadísticas finales
    catalog['load_time'] = time.time() - start_time
    
    return {
        'total_deliveries': catalog['total_deliveries'],
        'total_delivery_persons': mp.size(catalog['last_delivery']),
        'total_nodes': mp.size(catalog['nodes']),
        'total_edges': catalog['total_edges'],
        'total_restaurants': al.size(catalog['restaurants']),
        'total_delivery_locations': al.size(catalog['delivery_locations']),
        'avg_delivery_time': catalog['total_time'] / catalog['total_deliveries'] if catalog['total_deliveries'] > 0 else 0,
        'execution_time': catalog['load_time']
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
