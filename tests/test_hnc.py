import pytest


@pytest.fixture
def G():
    import networkx as nx

    G = nx.Graph()

    G.add_nodes_from(range(4))
    G.add_edge(0, 2, weight=1)
    G.add_edge(1, 2, weight=2)
    G.add_edge(2, 3, weight=5)

    return G


@pytest.fixture
def HNC(G):
    from closure.hnc import HNC

    return HNC(G, [0, 1], [3, ])


def test_HNC_single_value(HNC):
    set = HNC.solve(0.0)

    assert set == {0, 1}


def test_HNC_parametric(HNC):
    sets, breakpoints = HNC.solve_parametric(0, 5.0)

    assert breakpoints == [0.25, 5.0]
    assert sets[0] == {0, 1}
    assert sets[1] == {0, 1, 2}
