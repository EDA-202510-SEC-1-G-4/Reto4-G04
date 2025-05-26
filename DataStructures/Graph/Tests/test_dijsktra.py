from DataStructures.Graph import digraph as gl
from DataStructures.Map import map_linear_probing as map

from DataStructures.Graph import dijsktra_search as djk
from DataStructures.Stack import stack as stk
from DataStructures.Utils.utils import handle_not_implemented


def setup_tests():
    empty_graph = gl.new_graph()

    basic_graph = gl.new_graph(5)
    vertices = map.new_map(5, 0.5)
    vertices["scale"] = 1
    vertices["shift"] = 0
    informacion = map.new_map(5, 0.5)
    informacion["scale"] = 1
    informacion["shift"] = 0
    in_degree = map.new_map(5, 0.5)
    in_degree["scale"] = 1
    in_degree["shift"] = 0
    basic_graph["vertices"] = vertices
    basic_graph["informacion"] = informacion
    basic_graph["in_degree"] = in_degree

    for i in range(1, 6):
        gl.insert_vertex(basic_graph, i, {"name": i})
    gl.add_edge(basic_graph, 1, 2, 4)
    gl.add_edge(basic_graph, 1, 3, 2)
    gl.add_edge(basic_graph, 3, 2, 1)
    gl.add_edge(basic_graph, 2, 4, 5)
    gl.add_edge(basic_graph, 3, 4, 8)
    gl.add_edge(basic_graph, 4, 5, 3)

    return empty_graph, basic_graph

@handle_not_implemented
def test_dijkstra():
    empty_graph, graph = setup_tests()

    result = djk.dijkstra(graph, 1)
    assert result["source"] == 1
    assert result["visited"] is not None
    assert result["pq"] is not None

    # Verifica distancia mínima a cada nodo
    assert djk.dist_to(2, result) == 3  # 1->3->2
    assert djk.dist_to(4, result) == 8  # 1->3->2->4
    assert djk.dist_to(5, result) == 11

    # Verifica si hay camino
    assert djk.has_path_to(5, result) is True
    assert djk.has_path_to(99, result) is False

    # Verifica el camino correcto
    path = djk.path_to(5, result)
    assert stk.pop(path) == 1
    assert stk.pop(path) == 3 
    # Y así sucesivamente, o simplemente:
    assert stk.pop(path) == 2  # destino correcto

    assert stk.pop(path) == 4
    assert stk.pop(path) == 5

