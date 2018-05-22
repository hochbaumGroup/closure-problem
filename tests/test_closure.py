import pytest
import networkx as nx


@pytest.fixture
def G():
    G = nx.DiGraph()

    G.add_node(0, weight=3, multiplier=0)
    G.add_node(1, weight=-6, multiplier=0)
    G.add_node(2, weight=4, multiplier=2)

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


@pytest.fixture
def C_parametric(G):
    from closure.closure import Closure

    return Closure(G, node_weight=('weight', 'multiplier'))


def test_min_closure(C):
    set = C.solve()

    assert set == {1, 2}


def test_min_s_excess(S_Excess):
    set = S_Excess.solve()

    assert set == {1, }


def test_min_closure_parametric(C_parametric):
    sets, breakpoints = C_parametric.solve_parametric(0, 5)

    assert breakpoints == [1, 5.0]
    assert sets[0] == {1, 2}
    assert sets[1] == set()
