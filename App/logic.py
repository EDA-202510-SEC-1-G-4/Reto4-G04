import time
import csv
import time
from DataStructures.Graph import digraph as G
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al
from DataStructures.Graph import edge as edg  

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    catalog = {
        'graph': G.new_graph(),
        'delivery_persons': mp.new_map(100),  # Para almacenar información de domiciliarios
        'deliveries_count': 0,                # Contador de domicilios procesados
        'last_delivery': mp.new_map(100),     # Para rastrear último destino por domiciliario
        'restaurants': mp.new_map(100),       # Para contar restaurantes únicos
        'delivery_locations': mp.new_map(100) # Para contar ubicaciones de entrega únicas
    }
    return catalog


# Funciones para la carga de datos
def format_coordinate(coord):
    """
    Formatea una coordenada (latitud o longitud) a 4 decimales
    """
    try:
        return "{0:.4f}".format(float(coord))
    except:
        return "0.0000"

def create_node_id(lat, lon):
    """
    Crea un ID de nodo en formato "<Latitud>_<Longitud>" con 4 decimales
    """
    lat_formatted = format_coordinate(lat)
    lon_formatted = format_coordinate(lon)
    return f"{lat_formatted}_{lon_formatted}"


def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    start_time = get_time()
    
    # Inicializar estructuras para estadísticas
    total_time = 0
    delivery_person_set = set()
    csvfile = open(filename,'r',encoding='utf-8')
    reader = csv.DictReader(csvfile)
        
    for row in reader:
        # Procesar cada fila del CSV
        catalog['deliveries_count'] += 1
                
        # Obtener datos del domiciliario
        delivery_person_id = row['Delivery_person_ID']
        delivery_person_set.add(delivery_person_id)
                
        # Crear IDs de nodos para origen y destino
        rest_lat = row['Restaurant_latitude']
        rest_lon = row['Restaurant_longitude']
        deliv_lat = row['Delivery_location_latitude']
        deliv_lon = row['Delivery_location_longitude']
                
        origin_id = create_node_id(rest_lat, rest_lon)
        dest_id = create_node_id(deliv_lat, deliv_lon)
                
         # Obtener tiempo de entrega
        time_taken = float(row['Time_taken(min)'])
        total_time += time_taken
                
        # Agregar restaurante a la lista de restaurantes únicos
        if not mp.contains(catalog['restaurants'], origin_id):
            mp.put(catalog['restaurants'], origin_id, True)
                
        # Agregar ubicación de entrega a la lista de ubicaciones únicas
        if not mp.contains(catalog['delivery_locations'], dest_id):
            mp.put(catalog['delivery_locations'], dest_id, True)
                
        # Crear nodos si no existen
        if not G.contains_vertex(catalog['graph'], origin_id):
            G.insert_vertex(catalog['graph'], origin_id, {
                'type': 'restaurant',
                'delivery_persons': set()})
                
        if not G.contains_vertex(catalog['graph'], dest_id):
            G.insert_vertex(catalog['graph'], dest_id, {
                'type': 'delivery_location',
                'delivery_persons': set()})
                
        # Agregar domiciliario a los nodos
        origin_vertex = G.get_vertex(catalog['graph'], origin_id)
        origin_vertex['value']['delivery_persons'].add(delivery_person_id)
                
        dest_vertex = G.get_vertex(catalog['graph'], dest_id)
        dest_vertex['value']['delivery_persons'].add(delivery_person_id)
                
        # Agregar arco entre origen y destino (no dirigido)
        # Verificar si ya existe un arco entre estos nodos
        edge_origin = mp.contains(origin_vertex['adjacents'], dest_id)
        edge_dest = mp.contains(dest_vertex['adjacents'], origin_id)
                
        if edge_origin:
            # Si ya existe, calcular nuevo peso como promedio
            edge_origin = mp.get(origin_vertex['adjacents'], dest_id)
            edge_dest = mp.get(dest_vertex['adjacents'], origin_id)
                    
            current_weight = edge_origin['weight']
            new_weight = (current_weight + time_taken) / 2
                    
            edg.set_weight(edge_origin, new_weight)
            edg.set_weight(edge_dest, new_weight)
        else:
            # Si no existe, crear nuevos arcos
            G.add_edge(catalog['graph'], origin_id, dest_id, time_taken)
            G.add_edge(catalog['graph'], dest_id, origin_id, time_taken)
                
        # Agregar arco entre el destino actual y el último destino del mismo domiciliario
        if mp.contains(catalog['last_delivery'], delivery_person_id):
            last_dest_id = mp.get(catalog['last_delivery'], delivery_person_id)
                    
            if last_dest_id != dest_id:  # Evitar autociclos
                last_dest_vertex = G.get_vertex(catalog['graph'], last_dest_id)
                        
                # Verificar si ya existe un arco
                existing_edge_last = mp.contains(dest_vertex['adjacents'], last_dest_id)
                edge_current = mp.contains(last_dest_vertex['adjacents'], dest_id)
                        
                if existing_edge_last:
                    # Calcular nuevo peso como promedio
                    edge_last = mp.get(dest_vertex['adjacents'], last_dest_id)
                    edge_current = mp.get(last_dest_vertex['adjacents'], dest_id)
                            
                    current_weight = edge_last['weight']
                    new_weight = (current_weight + time_taken) / 2
                            
                    edg.set_weight(edge_last, new_weight)
                    edg.set_weight(edge_current, new_weight)
                else:
                    # Crear nuevos arcos
                    avg_time = time_taken  # En este caso simple usamos el tiempo actual
                    G.add_edge(catalog['graph'], dest_id, last_dest_id, avg_time)
                    G.add_edge(catalog['graph'], last_dest_id, dest_id, avg_time)
                
        # Actualizar último destino del domiciliario
        mp.put(catalog['last_delivery'], delivery_person_id, dest_id)
    
    end_time = get_time()
    
    # Calcular estadísticas
    stats = {
        'total_deliveries': catalog['deliveries_count'],
        'total_delivery_persons': len(delivery_person_set),
        'total_nodes': G.order(catalog['graph']),
        'total_edges': G.size(catalog['graph']) // 2,  # Dividido por 2 porque es no dirigido
        'total_restaurants': mp.size(catalog['restaurants']),
        'total_delivery_locations': mp.size(catalog['delivery_locations']),
        'avg_delivery_time': total_time / catalog['deliveries_count'] if catalog['deliveries_count'] > 0 else 0,
        'execution_time': delta_time(start_time, end_time)
    }
    
    return stats
    
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
