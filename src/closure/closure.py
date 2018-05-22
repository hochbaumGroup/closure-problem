import networkx as nx
from pseudoflow import hpf


class Closure(object):
    """Class for closure problems on directed graphs

    NOTE: Only works correctly when source adjacent arcs have increasing
    parameter weights and sink adjacent arcs have negative parameter weights.

    """

    def __init__(self, graph, node_weight='weight', arc_weight=None):
        if arc_weight is None:
            arc_weight = 'weight'
            for u, v in graph.edges:
                graph[u][v]['weight'] = float('inf')

        graph.add_nodes_from(['s', 't'])

        if isinstance(node_weight, str):
            constant = node_weight
            multiplier = None
        else:
            constant, multiplier = node_weight

        if multiplier:
            for u, v in graph.edges:
                graph[u][v]['multiplier'] = 0

            for node in graph.nodes:
                if node not in ('s', 't'):
                    weight = graph.nodes[node][constant]
                    multiplier_weight = graph.nodes[node][multiplier]
                    graph.add_edge(node, 't',
                                   **{arc_weight: weight,
                                      'multiplier': multiplier_weight})
                    graph.add_edge('s', node,
                                   **{arc_weight: -weight,
                                      'multiplier': -multiplier_weight})
        else:
            for node in graph.nodes:
                if node not in ('s', 't'):
                    weight = graph.nodes[node][constant]
                    if weight > 0:
                        graph.add_edge(node, 't',
                                       **{arc_weight: weight})
                    elif weight < 0:
                        graph.add_edge('s', node,
                                       **{arc_weight: -weight})

        self._G = graph
        self._constant = constant
        self._arc_weight = arc_weight

    def solve(self):
        _, cuts, _ = hpf(self._G, 's', 't', self._arc_weight)

        return {x for x in self._G if cuts[x][0] == 1 and x not in ('s', 't')}

    def solve_parametric(self, parameter_range):
        breakpoints, cuts, _ = hpf(
            self._G, 's', 't', self._arc_weight, mult_cap='multiplier',
            lambdaRange=parameter_range, roundNegativeCapacity=True)

        cuts = [
            {x for x in self._G if cuts[x][i] == 1 and x not in ('s', 't')}
            for i in range(len(breakpoints))
        ]

        return cuts, breakpoints
