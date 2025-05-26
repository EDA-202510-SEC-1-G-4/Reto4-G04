import sys
import csv
import os
from tabulate import tabulate
from DataStructures.Graph import digraph as G
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import edge as edg

def new_logic():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función de la lógica donde se crean las estructuras de datos
    control = {
        'graph': G.new_graph(),
        'delivery_persons': mp.new_map(100),
        'deliveries_count': 0,
        'last_delivery': mp.new_map(100),
        'restaurants': mp.new_map(100),
        'delivery_locations': mp.new_map(100),
        'delivery_person_set': set()
    }
    return control
    
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
    Carga los datos directamente desde el archivo CSV
    """
    print("\n=== CARGAR DATOS ===")
    print("Coloque su archivo CSV en la misma carpeta que este programa")
    print("Archivos CSV disponibles en el directorio actual:")
    
    # Listar archivos CSV disponibles
    csv_files = [f for f in os.listdir() if f.endswith('.csv')]
    if not csv_files:
        print("No se encontraron archivos CSV en el directorio actual")
        return False
    
    for i, filename in enumerate(csv_files, 1):
        print(f"{i}. {filename}")
    
    while True:
        try:
            selection = input("\nIngrese el número del archivo a cargar (0 para cancelar): ")
            if selection == '0':
                return False
            
            filename = csv_files[int(selection)-1]
            break
        except (ValueError, IndexError):
            print("Selección inválida. Intente nuevamente.")
    
    start_time = get_time()
    total_time = 0
    
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                try:
                    # Procesar cada fila del CSV
                    control['deliveries_count'] += 1
                    
                    # Registrar domiciliario
                    delivery_person_id = row['Delivery_person_ID']
                    control['delivery_person_set'].add(delivery_person_id)
                    
                    # Crear IDs de nodos
                    origin_id = create_node_id(
                        row['Restaurant_latitude'], 
                        row['Restaurant_longitude']
                    )
                    dest_id = create_node_id(
                        row['Delivery_location_latitude'], 
                        row['Delivery_location_longitude']
                    )
                    
                    # Registrar tiempo
                    time_taken = float(row['Time_taken(min)'])
                    total_time += time_taken
                    
                    # Registrar restaurantes y ubicaciones únicas
                    if not mp.contains(control['restaurants'], origin_id):
                        mp.put(control['restaurants'], origin_id, True)
                    
                    if not mp.contains(control['delivery_locations'], dest_id):
                        mp.put(control['delivery_locations'], dest_id, True)
                    
                    # Crear nodos si no existen
                    if not G.contains_vertex(control['graph'], origin_id):
                        G.insert_vertex(control['graph'], origin_id, {
                            'type': 'restaurant',
                            'delivery_persons': set()
                        })
                    
                    if not G.contains_vertex(control['graph'], dest_id):
                        G.insert_vertex(control['graph'], dest_id, {
                            'type': 'delivery_location',
                            'delivery_persons': set()
                        })
                    
                    # Obtener vértices
                    origin_vertex = G.get_vertex(control['graph'], origin_id)
                    dest_vertex = G.get_vertex(control['graph'], dest_id)
                    
                    # Agregar domiciliario a los nodos
                    origin_vertex['value']['delivery_persons'].add(delivery_person_id)
                    dest_vertex['value']['delivery_persons'].add(delivery_person_id)
                    
                    # Agregar arco entre origen y destino (no dirigido)
                    existing_edge_origin = mp.contains(origin_vertex['adjacents'], dest_id)
                    existing_edge_dest = mp.contains(dest_vertex['adjacents'], origin_id)
                    
                    if existing_edge_origin:
                        # Si ya existe, calcular nuevo peso como promedio
                        edge_origin = mp.get(origin_vertex['adjacents'], dest_id)
                        edge_dest = mp.get(dest_vertex['adjacents'], origin_id)
                        
                        current_weight = edge_origin['weight']
                        new_weight = (current_weight + time_taken) / 2
                        
                        edg.set_weight(edge_origin, new_weight)
                        edg.set_weight(edge_dest, new_weight)
                    else:
                        # Si no existe, crear nuevos arcos
                        G.add_edge(control['graph'], origin_id, dest_id, time_taken)
                        G.add_edge(control['graph'], dest_id, origin_id, time_taken)
                    
                    # Registrar último destino del domiciliario
                    if mp.contains(control['last_delivery'], delivery_person_id):
                        last_dest_id = mp.get(control['last_delivery'], delivery_person_id)
                        
                        if last_dest_id != dest_id:  # Evitar autociclos
                            last_dest_vertex = G.get_vertex(control['graph'], last_dest_id)
                            
                            # Verificar si ya existe un arco
                            existing_edge_last = mp.contains(dest_vertex['adjacents'], last_dest_id)
                            existing_edge_current = mp.contains(last_dest_vertex['adjacents'], dest_id)
                            
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
                                G.add_edge(control['graph'], dest_id, last_dest_id, time_taken)
                                G.add_edge(control['graph'], last_dest_id, dest_id, time_taken)
                    
                    mp.put(control['last_delivery'], delivery_person_id, dest_id)
                    
                except Exception as e:
                    print(f"Error procesando fila: {str(e)}")
                    continue
        
        end_time = get_time()
        
        # Calcular estadísticas
        stats = {
            'total_deliveries': control['deliveries_count'],
            'total_delivery_persons': len(control['delivery_person_set']),
            'total_nodes': G.order(control['graph']),
            'total_edges': G.size(control['graph']) // 2,  # Dividido por 2 por ser no dirigido
            'total_restaurants': mp.size(control['restaurants']),
            'total_delivery_locations': mp.size(control['delivery_locations']),
            'avg_delivery_time': total_time / control['deliveries_count'] if control['deliveries_count'] > 0 else 0,
            'execution_time': delta_time(start_time, end_time)
        }
        
        # Mostrar resultados
        print("\n" + "="*50)
        print("RESULTADOS DE LA CARGA DE DATOS")
        print("="*50)
        
        stats_table = [
            ["Domicilios procesados", stats['total_deliveries']],
            ["Domiciliarios únicos", stats['total_delivery_persons']],
            ["Nodos en el grafo", stats['total_nodes']],
            ["Arcos en el grafo", stats['total_edges']],
            ["Restaurantes únicos", stats['total_restaurants']],
            ["Ubicaciones de entrega", stats['total_delivery_locations']],
            ["Tiempo promedio (min)", f"{stats['avg_delivery_time']:.2f}"],
            ["Tiempo de carga (ms)", f"{stats['execution_time']:.2f}"]
        ]
        
        print(tabulate(stats_table, headers=["Métrica", "Valor"], tablefmt="grid"))
        print("="*50 + "\n")
        
        return True
        
    except FileNotFoundError:
        print(f"\nERROR: Archivo '{filename}' no encontrado.")
        print("Asegúrese que el archivo esté en el mismo directorio que este programa.\n")
        return False
    except Exception as e:
        print(f"\nERROR inesperado: {str(e)}\n")
        return False

def get_time():
    """Devuelve el instante tiempo de procesamiento en milisegundos"""
    import time
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
control = new_logic()

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
