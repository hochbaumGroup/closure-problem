import networkx as nx

import pytest

from closure.hnc import HNC


@pytest.fixture
def G():
    G = nx.Graph()

    G.add_nodes_from(range(4))
    G.add_edge(0, 2, weight=1)
    G.add_edge(1, 2, weight=2)
    G.add_edge(2, 3, weight=5)
    return G


def test_HNC_single_value(G):
    assert HNC(G, [0, 1], [3, ]).solve(0.0) == {0, 1}


def test_HNC_parametric(G):
    sets, breakpoints = HNC(G, [0, 1], [3, ]).solve_parametric(0, 5.0)

    assert breakpoints == [0.25, 5.0]
    assert sets[0] == {0, 1}
    assert sets[1] == {0, 1, 2}


def test_HNC_input_graph_should_not_change(G):
    assert HNC(G, [0, 1], [3, ]).solve(0.0) == {0, 1}

    assert 'degree' not in G.nodes[0]
    assert G.number_of_nodes() == 4

