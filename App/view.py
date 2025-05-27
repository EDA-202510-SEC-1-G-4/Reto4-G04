import sys
import csv
import os
import time
from tabulate import tabulate
from DataStructures.Graph import digraph as G
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import edge as edg
from App import logic as log
    
def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8 (Bono)")
    print("0- Salir")


def format_coordinate(coord):
    """Formatea una coordenada a 4 decimales"""
    try:
        return "{0:.4f}".format(float(coord))
    except:
        return "0.0000"

def create_node_id(lat, lon):
    """Crea un ID de nodo en formato 'lat_lon' con 4 decimales"""
    return f"{format_coordinate(lat)}_{format_coordinate(lon)}"


def load_data(control):
    """
    Carga los datos desde el archivo CSV seleccionado por el usuario
    y muestra estadísticas de carga.
    """
    print("Cargando información de los archivos...")

    # Solicitar al usuario el tamaño del archivo a cargar
    print("\nSeleccione el tamaño del archivo a cargar:")
    print("1- Pequeño (deliverytime_min.csv)")
    print("2- Mediano (deliverytime_10.csv)")
    print("3- Grande (deliverytime_large.csv)")
    size_option = input("Ingrese su opción (1-3): ")

    filename = ""
    if size_option == "1":
        filename = "deliverytime_min.csv"
    elif size_option == "2":
        filename = "deliverytime_10.csv"
    elif size_option == "3":
        filename = "deliverytime_large.csv"
    else:
        print("Opción inválida, se cargará el archivo pequeño por defecto")
        filename = "deliverytime_min.csv"

    # Cargar los datos
    stats = log.load_data(control, filename)

    # Mostrar estadísticas de carga
    print("Estadísticas de Carga")

    stats_table = [
        ["Total de domicilios procesados", stats['total_deliveries']],
        ["Total de domiciliarios únicos", stats['total_delivery_persons']],
        ["Total de nodos en el grafo", stats['total_nodes']],
        ["Total de arcos en el grafo", stats['total_edges']],
        ["Total de restaurantes únicos", stats['total_restaurants']],
        ["Total de ubicaciones de entrega únicas", stats['total_delivery_locations']],
        ["Tiempo promedio de entrega (min)", f"{stats['avg_delivery_time']:.2f}"],
        ["Tiempo de carga (ms)", f"{stats['load_time']:.2f}"]
    ]

    print(tabulate(stats_table))

def get_time():
    """Devuelve el instante tiempo de procesamiento en milisegundos"""
    return float(time.perf_counter()*1000)

def delta_time(start, end):
    """Devuelve la diferencia entre tiempos de procesamiento muestreados"""
    elapsed = float(end - start)
    return elapsed



def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea la lógica asociado a la vista
control = log.new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
