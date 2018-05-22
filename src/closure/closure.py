import networkx as nx
from pseudoflow import hpf


class Closure(object):
    """Class for closure problems on directed graphs

    NOTE: Only works correctly when source adjacent arcs have increasing
    parameter weights and sink adjacent arcs have negative parameter weights.

    """

    def __init__(self, graph, node_weight='weight', arc_weight=None,
                 source_node=None, sink_node=None):
        if arc_weight is None:
            arc_weight = 'weight'
            for u, v in graph.edges:
                graph[u][v]['weight'] = float('inf')

        if source_node is None:
            self._source_node = 'source'
            graph.add_node(self._source_node)
        else:
            self._source_node = source_node

        if sink_node is None:
            self._sink_node = 'sink'
            graph.add_node(self._sink_node)
        else:
            self._sink_node = sink_node

        if isinstance(node_weight, str):
            constant = node_weight
            multiplier = None
        else:
            constant, multiplier = node_weight

        if multiplier:
            for u, v in graph.edges:
                graph[u][v]['multiplier'] = 0

            for node in graph.nodes:
                if node not in (self._source_node, self._sink_node):
                    weight = graph.nodes[node][constant]
                    multiplier_weight = graph.nodes[node][multiplier]
                    graph.add_edge(node, self._sink_node,
                                   **{arc_weight: weight,
                                      'multiplier': multiplier_weight})
                    graph.add_edge(self._source_node, node,
                                   **{arc_weight: -weight,
                                      'multiplier': -multiplier_weight})
        else:
            for node in graph.nodes:
                if node not in (self._source_node, self._sink_node):
                    weight = graph.nodes[node][constant]
                    if weight > 0:
                        graph.add_edge(node, self._sink_node,
                                       **{arc_weight: weight})
                    elif weight < 0:
                        graph.add_edge(self._source_node, node,
                                       **{arc_weight: -weight})

        self._G = graph
        self._constant = constant
        self._arc_weight = arc_weight

    def _binary_cut_to_set(self, cut, index):
        return {x for x in self._G if cut[x][index] == 1 and x not in (self._source_node, 't')}

    def solve(self):
        _, cuts, _ = hpf(self._G, self._source_node, self._sink_node, self._arc_weight)

        return self._binary_cut_to_set(cuts, 0)

    def solve_parametric(self, parameter_range):
        breakpoints, cuts, _ = hpf(
            self._G, self._source_node, self._sink_node, self._arc_weight, mult_cap='multiplier',
            lambdaRange=parameter_range, roundNegativeCapacity=True)

        cuts = [
            self._binary_cut_to_set(cuts, i) for i in range(len(breakpoints))
        ]

        return cuts, breakpoints
