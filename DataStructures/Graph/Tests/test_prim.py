from DataStructures.Graph import adj_list_graph as gl
from DataStructures.Graph import prim as prim
from DataStructures.Graph import edge as ed
from DataStructures.Map import map_linear_probing as map
from DataStructures.Stack import stack as st
from DataStructures.Queue import queue as qu
from DataStructures.Priority_queue import index_priority_queue as pq
from DataStructures.Utils.utils import handle_not_implemented


def setup_tests():
    empty_graph = gl.new_graph()

    some_graph = gl.new_graph(6)

    # Al definir el scale y shift en 1 y 0 respectivamente, se garantiza que el hash de los vertices sea el mismo
    # en cada ejecución, permitiendo realizar las pruebas de manera consistente.
    vertices = map.new_map(6, 0.5)
    vertices["scale"] = 1
    vertices["shift"] = 0

    informacion = map.new_map(6, 0.5)
    informacion["scale"] = 1
    informacion["shift"] = 0

    in_degree = map.new_map(6, 0.5)
    in_degree["scale"] = 1
    in_degree["shift"] = 0

    some_graph["vertices"] = vertices
    some_graph["informacion"] = informacion
    some_graph["in_degree"] = in_degree

    gl.insert_vertex(some_graph, 1, {"name": "A"})
    gl.insert_vertex(some_graph, 2, {"name": "B"})
    gl.insert_vertex(some_graph, 3, {"name": "C"})
    gl.insert_vertex(some_graph, 4, {"name": "D"})
    gl.insert_vertex(some_graph, 5, {"name": "E"})
    gl.insert_vertex(some_graph, 6, {"name": "F"})

    gl.add_edge(some_graph, 1, 2, 7)
    gl.add_edge(some_graph, 1, 3, 5)
    gl.add_edge(some_graph, 1, 4, 4)
    gl.add_edge(some_graph, 2, 4, 2)
    gl.add_edge(some_graph, 3, 4, 5)
    gl.add_edge(some_graph, 3, 5, 3)
    gl.add_edge(some_graph, 3, 6, 10)
    gl.add_edge(some_graph, 4, 5, 3)
    gl.add_edge(some_graph, 5, 6, 2)

    return empty_graph, some_graph


@handle_not_implemented
def test_prim_mst():
    empty_graph, some_graph = setup_tests()

    search = prim.prim_mst(some_graph, 1)
    assert search["source"] == 1
    assert search["edge_to"] is not None
    assert search["dist_to"] is not None
    assert search["marked"] is not None
    assert search["pq"] is not None
    assert search["mst"] is not None

    assert qu.size(search["mst"]) == 0
    assert pq.size(search["edge_to"]) == 5


@handle_not_implemented
def test_edges_mst():
    empty_graph, some_graph = setup_tests()

    search = prim.prim_mst(some_graph, 1)
    mst = prim.edges_mst(some_graph, search)

    assert qu.size(mst) == 5
    vertex = set()
    for i in range(5):
        edge = qu.dequeue(mst)
        vertex.add(ed.either(edge))
        vertex.add(ed.other(edge, ed.either(edge)))
    assert len(vertex) == 6
    for i in range(1, 7):
        assert i in vertex


@handle_not_implemented
def test_wight_mst():
    empty_graph, some_graph = setup_tests()

    search = prim.prim_mst(some_graph, 1)
    weight = prim.weight_mst(some_graph, search)

    assert weight == 14
