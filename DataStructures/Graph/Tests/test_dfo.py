from DataStructures.Graph import adj_list_graph as g
from DataStructures.Graph import dfo as dfo
from DataStructures.Map import map_linear_probing as map
from DataStructures.Stack import stack as stk
from DataStructures.Utils.utils import handle_not_implemented


def setup_tests():
    my_graph = g.new_graph(7, True)

    # Al definir el scale y shift en 1 y 0 respectivamente, se garantiza que el hash de los vertices sea el mismo
    # en cada ejecución, permitiendo realizar las pruebas de manera consistente.
    vertices = map.new_map(7, 0.5)
    vertices["scale"] = 1
    vertices["shift"] = 0

    informacion = map.new_map(7, 0.5)
    informacion["scale"] = 1
    informacion["shift"] = 0

    in_degree = map.new_map(7, 0.5)
    in_degree["scale"] = 1
    in_degree["shift"] = 0

    my_graph["vertices"] = vertices
    my_graph["informacion"] = informacion
    my_graph["in_degree"] = in_degree

    for i in range(1, 8):
        g.insert_vertex(my_graph, i, {"name": i})

    g.add_edge(my_graph, 1, 2, 1)
    g.add_edge(my_graph, 2, 3, 1)
    g.add_edge(my_graph, 2, 4, 1)
    g.add_edge(my_graph, 3, 1, 1)
    g.add_edge(my_graph, 4, 3, 1)
    g.add_edge(my_graph, 5, 2, 1)
    g.add_edge(my_graph, 6, 3, 1)
    g.add_edge(my_graph, 6, 4, 1)
    g.add_edge(my_graph, 7, 4, 1)
    g.add_edge(my_graph, 7, 5, 1)

    return my_graph


@handle_not_implemented
def test_depth_first_order():
    my_graph = setup_tests()
    new_dfo = dfo.depth_first_order(my_graph)

    assert new_dfo["marked"] is not None
    assert new_dfo["pre"] is not None
    assert new_dfo["post"] is not None
    assert new_dfo["reversepost"] is not None

    assert stk.size(new_dfo["reversepost"]) == 7
    assert stk.pop(new_dfo["reversepost"]) == 7
    assert stk.pop(new_dfo["reversepost"]) == 6
    assert stk.pop(new_dfo["reversepost"]) == 5
    assert stk.pop(new_dfo["reversepost"]) == 1
    assert stk.pop(new_dfo["reversepost"]) == 2
    assert stk.pop(new_dfo["reversepost"]) == 4
    assert stk.pop(new_dfo["reversepost"]) == 3
