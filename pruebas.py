from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import bfs
from DataStructures.Graph import digraph as G
from DataStructures.Graph import vertex as V
from DataStructures.Stack import stack as s

# Crear grafo vacío
grafo = G.new_graph(10)

# Crear vértices con key y value
v1 = V.new_vertex(1, {"name": 1})
v2 = V.new_vertex(2, {"name": 2})
v3 = V.new_vertex(3, {"name": 3})

# Insertar vértices al grafo
mp.put(grafo['vertices'], 1, v1)
mp.put(grafo['vertices'], 2, v2)
mp.put(grafo['vertices'], 3, v3)

# Conectar adyacencias
mp.put(v1["adjacents"], 2, {"to": 2, "weight": 1})
mp.put(v2["adjacents"], 3, {"to": 3, "weight": 1})

# Ejecutar BFS desde 1
search = bfs.bfs(grafo, 1)

# Mostrar vértices visitados
print("Visitados:")
for i in range(mp.size(search["visited"])):
    key = mp.get(mp.key_set(search["visited"]), i)["value"]
    print("-", key)

# Mostrar predecesores
print("Predecesores:")
for i in range(mp.size(search["edgeTo"])):
    key = mp.get(mp.key_set(search["edgeTo"]), i)["value"]
    pred = mp.get(search["edgeTo"], key)["value"]
    print(f"{key} <- {pred}")

# Mostrar camino de 1 a 3
print("Camino de 1 a 3:")
path = bfs.path_to(3, search)
while not s.is_empty(path):
    print(s.pop(path))
