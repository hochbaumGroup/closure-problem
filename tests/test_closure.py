import pytest
import networkx as nx

from closure.closure import Closure


@pytest.fixture
def G():
    G = nx.DiGraph()

    G.add_node(0, weight=3)
    G.add_node(1, weight=-6)
    G.add_node(2, weight=4)

    G.add_edge(0, 1, weight=1)
    G.add_edge(0, 2, weight=1)
    G.add_edge(1, 2, weight=1)

    return G

def test_min_closure(G):
    assert Closure(G).solve() == {1, 2}


def test_min_s_excess(G):
    assert Closure(G, arc_weight='weight').solve() == {1, }


def test_min_closure_parametric():
    G = nx.DiGraph()

    G.add_node(0, weight=3, multiplier=0)
    G.add_node(1, weight=-6, multiplier=0)
    G.add_node(2, weight=8, multiplier=-1)

    G.add_edge(0, 1, weight=1)
    G.add_edge(0, 2, weight=1)
    G.add_edge(1, 2, weight=1)

    sets, breakpoints = Closure(G, node_weight=('weight', 'multiplier')).solve_parametric(0, 3)

    assert breakpoints == [2, 3.0]
    assert sets[0] == set()
    assert sets[1] == {1, 2}
