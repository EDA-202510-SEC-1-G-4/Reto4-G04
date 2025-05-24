from DataStructures.Graph import dfs as dfs
from DataStructures.Graph import adj_list_graph as g
from DataStructures.Map import map_linear_probing as map
from DataStructures.Stack import stack as stk
from DataStructures.Utils.utils import handle_not_implemented


def setup_tests():
    my_graph = g.new_graph(9)

    for i in range(1, 10):
        g.insert_vertex(my_graph, i, {"name": i})

    g.add_edge(my_graph, 1, 2, 1)
    g.add_edge(my_graph, 1, 4, 1)
    g.add_edge(my_graph, 1, 5, 1)
    g.add_edge(my_graph, 2, 3, 1)
    g.add_edge(my_graph, 2, 5, 1)
    g.add_edge(my_graph, 3, 6, 1)
    g.add_edge(my_graph, 4, 7, 1)
    g.add_edge(my_graph, 5, 6, 1)
    g.add_edge(my_graph, 5, 7, 1)
    g.add_edge(my_graph, 5, 8, 1)
    g.add_edge(my_graph, 5, 9, 1)
    g.add_edge(my_graph, 6, 9, 1)
    g.add_edge(my_graph, 7, 8, 1)
    g.add_edge(my_graph, 8, 9, 1)

    no_conected = g.new_graph(5)
    for i in range(1, 6):
        g.insert_vertex(no_conected, i, {"name": i})

    g.add_edge(no_conected, 1, 2, 1)
    g.add_edge(no_conected, 1, 3, 1)
    g.add_edge(no_conected, 1, 4, 1)

    return my_graph, no_conected


@handle_not_implemented
def test_depth_first_search():
    my_graph, n = setup_tests()
    new_dfs = dfs.depth_first_search(my_graph, 1)
    assert new_dfs["source"] == 1
    assert new_dfs["visited"] is not None
    assert map.get(new_dfs["visited"], 1) == {"marked": True, "edge_to": None}
    assert map.get(new_dfs["visited"], 2) == {"marked": True, "edge_to": 1}
    assert map.get(new_dfs["visited"], 3) == {"marked": True, "edge_to": 2}
    assert map.get(new_dfs["visited"], 4) == {"marked": True, "edge_to": 7}
    assert map.get(new_dfs["visited"], 5) == {"marked": True, "edge_to": 6}
    assert map.get(new_dfs["visited"], 6) == {"marked": True, "edge_to": 3}
    assert map.get(new_dfs["visited"], 7) == {"marked": True, "edge_to": 5}
    assert map.get(new_dfs["visited"], 8) == {"marked": True, "edge_to": 7}
    assert map.get(new_dfs["visited"], 9) == {"marked": True, "edge_to": 8}


@handle_not_implemented
def test_has_path_to():
    my_graph, no_conected = setup_tests()
    new_dfs = dfs.depth_first_search(my_graph, 1)
    for i in range(1, 10):
        assert dfs.has_path_to(new_dfs, i) is True

    new_dfs = dfs.depth_first_search(no_conected, 1)
    assert dfs.has_path_to(new_dfs, 1) is True
    assert dfs.has_path_to(new_dfs, 2) is True
    assert dfs.has_path_to(new_dfs, 3) is True
    assert dfs.has_path_to(new_dfs, 4) is True
    assert dfs.has_path_to(new_dfs, 5) is False


@handle_not_implemented
def test_path_to():
    my_graph, no_conected = setup_tests()
    new_dfs = dfs.depth_first_search(my_graph, 1)
    path = dfs.path_to(new_dfs, 2)

    assert path is not None
    assert stk.size(path) == 2
    assert stk.pop(path) == 1
    assert stk.pop(path) == 2

    path = dfs.path_to(new_dfs, 3)
    assert path is not None
    assert stk.size(path) == 3
    assert stk.pop(path) == 1
    assert stk.pop(path) == 2
    assert stk.pop(path) == 3

    path = dfs.path_to(new_dfs, 4)
    assert path is not None
    assert stk.size(path) == 7
    assert stk.pop(path) == 1
    assert stk.pop(path) == 2
    assert stk.pop(path) == 3
    assert stk.pop(path) == 6
    assert stk.pop(path) == 5
    assert stk.pop(path) == 7
    assert stk.pop(path) == 4

    path = dfs.path_to(new_dfs, 9)
    assert path is not None
    assert stk.size(path) == 8
    assert stk.pop(path) == 1
    assert stk.pop(path) == 2
    assert stk.pop(path) == 3
    assert stk.pop(path) == 6
    assert stk.pop(path) == 5
    assert stk.pop(path) == 7
    assert stk.pop(path) == 8
    assert stk.pop(path) == 9
