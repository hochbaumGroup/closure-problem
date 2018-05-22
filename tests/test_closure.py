import pytest
import networkx as nx


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


@pytest.fixture
def C(G):
    from closure.closure import Closure

    return Closure(G)


@pytest.fixture
def S_Excess(G):
    from closure.closure import Closure

    return Closure(G, arc_weight='weight')


def test_min_closure(C):
    set = C.solve()
    print(set)

    assert 1 in set
    assert 2 in set
    assert len(set) == 2


def test_min_s_excess(S_Excess):
    set = S_Excess.solve()
    print(set)

    assert 1 in set
    assert len(set) == 1
