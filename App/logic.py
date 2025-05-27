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
        'deliveries': al.new_list(),
        'graph': G.new_graph(100),
        'nodes': mp.new_map(1000),  # Para almacenar nodos de ubicación
        'domiciliarios_ultimos_destinos': mp.new_map(100),
        'domiciliarios_ultimos_tiempos': mp.new_map(100),
        'restaurant_locations': al.new_list(),
        'delivery_locations': al.new_list(),
        'total_delivery_time': 0.0,
        'total_deliveries': 0,
        'load_time': 0.0,
        'total_edges': 0
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
            catalog['graph'] = G.insert_vertex(catalog['graph'], origin, al.new_list())
        if not G.contains_vertex(catalog['graph'], destination):
            catalog['graph'] = G.insert_vertex(catalog['graph'], destination, al.new_list())

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
        if edge is None:
            catalog['graph'] = G.add_edge(catalog['graph'], origin, destination, time_taken)
            catalog['graph'] = G.add_edge(catalog['graph'], destination, origin, time_taken)
            catalog['total_edges'] += 1
        else:
            avg = (edge['weight'] + time_taken) / 2
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
    catalog['total_delivery_persons'] = mp.size(catalog['domiciliarios_ultimos_destinos'])
    catalog['total_nodes'] = G.order(catalog['graph'])
    catalog['avg_delivery_time'] = catalog['total_delivery_time'] / catalog['total_deliveries']
    catalog['total_restaurants'] = al.size(catalog['restaurant_locations'])
    catalog['total_delivery_locations'] = al.size(catalog['delivery_locations'])

    return catalog


    
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
