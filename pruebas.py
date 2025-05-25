from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import bfs
from DataStructures.Graph import dfs
from DataStructures.Graph import digraph as g
from DataStructures.Graph import vertex as V
from DataStructures.Stack import stack as s


grafo = g.new_graph(8)
for i in range(1, 10):
    g.insert_vertex(grafo, i, {"name": i})

g.add_edge(grafo, 1, 2, 1)
g.add_edge(grafo, 1, 4, 1)
g.add_edge(grafo, 1, 5, 1)
g.add_edge(grafo, 2, 3, 1)
g.add_edge(grafo, 2, 5, 1)
g.add_edge(grafo, 3, 6, 1)
g.add_edge(grafo, 4, 7, 1)
g.add_edge(grafo, 5, 6, 1)
g.add_edge(grafo, 5, 7, 1)
g.add_edge(grafo, 5, 8, 1)
g.add_edge(grafo, 5, 9, 1)
g.add_edge(grafo, 6, 9, 1)
g.add_edge(grafo, 7, 8, 1)
g.add_edge(grafo, 8, 9, 1)


search = dfs.dfs(grafo, 1)
path = dfs.path_to(search, 3)

while not s.is_empty(path):
    elm = s.pop(path)
    print(f"sacando el elemento {elm}")