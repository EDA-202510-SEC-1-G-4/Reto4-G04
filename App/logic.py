import time
import csv
import time
from DataStructures.Graph import digraph as G
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al

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
    # TODO: Realizar la carga de datos
    
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
