from closure.closure import Closure


class HNC(object):
    def __init__(
        self,
        G,
        positive_seeds,
        negative_seeds,
        arc_weight="weight",
        node_label="degree",
    ):
        self._G = G
        self._arc_weight = arc_weight
        self._node_label_parametric = node_label
        self._node_label = "constant"

        self._positive_seeds = positive_seeds
        self._negative_seeds = negative_seeds

        self._add_node_weights()

        self._closure_problem = Closure(
            self._G.to_directed(),
            node_weight=(self._node_label, self._node_label_parametric),
            arc_weight=self._arc_weight,
            in_set=self._positive_seeds,
            not_in_set=self._negative_seeds,
        )

    def _add_node_weights(self):
        for node in self._G:
            self._G.nodes[node][self._node_label] = 0
            self._G.nodes[node][self._node_label_parametric] = -self._G.degree(
                node, weight=self._arc_weight
            )

    def solve(self, value):
        # solve for single value with same lower/upper bound
        cuts, breakpoints = self._closure_problem.solve_parametric(value, value)

        return cuts[0]

    def solve_parametric(self, low, high):
        # solve for single value with same lower/upper bound
        cuts, breakpoints = self._closure_problem.solve_parametric(low, high)

        return cuts, breakpoints
