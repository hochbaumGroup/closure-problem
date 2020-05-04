import networkx as nx
from pseudoflow import hpf


class Closure(object):
    """Class for closure problems on directed graphs

    NOTE: Only works correctly when source adjacent arcs have increasing
    parameter weights and sink adjacent arcs have negative parameter weights.

    Assumption: lambda >=0 and weight + multiplier * lambda
    has the same sign as weight + multiplier.

    """

    def __init__(
        self, graph, node_weight="weight", arc_weight=None, in_set=None, not_in_set=None
    ):
        if arc_weight is None:
            arc_weight = "weight"
            for u, v in graph.edges:
                graph[u][v]["weight"] = float("inf")

        self._source_node = "source"
        self._sink_node = "sink"
        self._special_nodes = (self._source_node, self._sink_node)
        self._G = graph
        self._arc_weight = arc_weight

        graph.add_nodes_from(self._special_nodes)

        if in_set is None:
            in_set = {}
        else:
            in_set = set(in_set)

        if not_in_set is None:
            not_in_set = {}
        else:
            not_in_set = set(not_in_set)

        if isinstance(node_weight, str):
            constant = node_weight
            multiplier = None
        else:
            constant, multiplier = node_weight
        self._constant = constant
        self._multiplier = multiplier

        if multiplier:
            for u, v in graph.edges:
                graph[u][v][multiplier] = 0

            for node in graph.nodes:
                if node in self._special_nodes:
                    pass
                elif node in in_set:
                    graph.add_edge(
                        self._source_node,
                        node,
                        **{arc_weight: float("inf"), self._multiplier: 0}
                    )
                elif node in not_in_set:
                    graph.add_edge(
                        node,
                        self._sink_node,
                        **{arc_weight: float("inf"), self._multiplier: 0}
                    )
                else:
                    weight = graph.nodes[node][constant]
                    multiplier_weight = graph.nodes[node][multiplier]
                    if weight + multiplier_weight > 0:
                        graph.add_edge(
                            node,
                            self._sink_node,
                            **{arc_weight: weight, self._multiplier: multiplier_weight}
                        )
                    elif weight + multiplier_weight < 0:
                        graph.add_edge(
                            self._source_node,
                            node,
                            **{
                                arc_weight: -weight,
                                self._multiplier: -multiplier_weight,
                            }
                        )
        else:
            for node in graph.nodes:
                if node in self._special_nodes:
                    pass
                elif node in in_set:
                    graph.add_edge(
                        self._source_node, node, **{arc_weight: float("inf")}
                    )
                elif node in not_in_set:
                    graph.add_edge(node, self._sink_node, **{arc_weight: float("inf")})
                else:
                    weight = graph.nodes[node][constant]
                    if weight > 0:
                        graph.add_edge(node, self._sink_node, **{arc_weight: weight})
                    elif weight < 0:
                        graph.add_edge(self._source_node, node, **{arc_weight: -weight})

    def _binary_cut_to_set(self, cut, index):
        return {
            x for x in self._G if cut[x][index] == 1 and x not in self._special_nodes
        }

    def solve(self):
        _, cuts, _ = hpf(
            self._G,
            self._source_node,
            self._sink_node,
            self._arc_weight,
            roundNegativeCapacity=True,
        )

        return self._binary_cut_to_set(cuts, 0)

    def solve_parametric(self, low, high):
        breakpoints, cuts, _ = hpf(
            self._G, self._source_node,
            self._sink_node, self._arc_weight, mult_cap=self._multiplier,
            lambdaRange=[low, high], roundNegativeCapacity=False)

        cuts = [
            self._binary_cut_to_set(cuts, i) for i in range(len(breakpoints))
        ]

        return cuts, breakpoints
