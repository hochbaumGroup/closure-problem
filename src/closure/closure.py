import networkx as nx
from pseudoflow import hpf


class Closure(object):
    """Class for closure problems on directed graphs"""

    def __init__(self, graph, node_weight='weight', arc_weight=None):
        if arc_weight is None:
            arc_weight = 'weight'
            for u, v in graph.edges:
                graph[u][v]['weight'] = float('inf')

        graph.add_nodes_from(['s', 't'])

        for node in graph.nodes:
            if node not in ('s', 't'):
                weight = graph.nodes[node][node_weight]
                if weight > 0:
                    graph.add_edge(node, 't',
                                   **{arc_weight: weight})
                elif weight < 0:
                    graph.add_edge('s', node,
                                   **{arc_weight: -weight})

        self._G = graph
        self._node_weight = node_weight
        self._arc_weight = arc_weight

    def solve(self):
        _, cuts, _ = hpf(self._G, 's', 't', self._arc_weight)

        print(cuts)

        return {x for x in self._G if cuts[x][0] == 1 and x not in ('s', 't')}
