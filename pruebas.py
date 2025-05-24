from DataStructures.Graph import digraph as G
 
# Crea un grafo vacío
my_graph = G.new_graph(1)

# Inserta vértices
my_graph = G.insert_vertex(my_graph, "Tunja", {"nombre": "Tunja", "poblacion": 200000})
my_graph = G.insert_vertex(my_graph, "Villavicencio", {"nombre": "Villavicencio", "poblacion": 300000})
my_graph = G.insert_vertex(my_graph, "Neiva", {"nombre": "Neiva", "poblacion": 350000})

# Inserta arcos
my_graph = G.add_edge(my_graph, "Tunja", "Villavicencio", 150)
my_graph = G.add_edge(my_graph, "Tunja", "Neiva", 180)

# Consulta de adyacencias
adj = G.adjacents(my_graph, "Tunja")
print(adj)
# Salida esperada: ['Villavicencio', 'Neiva']

# Consulta de adyacencias para un vértice sin conexiones
dj = G.adjacents(my_graph, "Neiva")
print(adj)
# Salida esperada: []

# Consulta de adyacencias para un vértice inexistente
try:
    adj = G.adjacents(my_graph, "Popayan")
except Exception as e:
    print(e)
# Salida esperada: El vertice no existe