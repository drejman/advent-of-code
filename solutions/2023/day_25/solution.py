# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/25

from collections import defaultdict
from copy import deepcopy
from math import prod
from random import shuffle

import networkx as nx

from ...base import StrSplitSolution, answer, timeit


class Solution(StrSplitSolution):
    _year = 2023
    _day = 25

    TARGET_EDGES = 3

    @timeit
    @answer(612945)
    def part_1(self) -> int:
        self._parse_input()
        edges = [[node, nn] for node in self.graph for nn in self.graph[node]]
        # return self.solve_using_networkx(edges=edges)

        while True:
            # Now we keep running Karger until we get what we want
            edges_per_node, nodesize = self.karger(deepcopy(edges))

            # We should now have exactly two nodes.
            # They should have identical sets of edges.
            if all(
                len(edges) <= self.TARGET_EDGES for edges in edges_per_node.values()
            ):
                break

        return prod(v for v in nodesize.values())

    @staticmethod
    def solve_using_networkx(edges):
        g = nx.Graph()
        g.add_edges_from(edges)
        g.remove_edges_from(nx.minimum_edge_cut(g))
        return prod([len(gi) for gi in nx.connected_components(g)])

    def karger(self, edges):
        # dict for fast access of edges by node
        edges_for_node = defaultdict(list)

        for edge in edges:
            edges_for_node[edge[0]].append(edge)
            edges_for_node[edge[1]].append(edge)

        nodesize = {key: 1 for key in edges_for_node.keys()}

        # By shuffling, we can simply pop edges off the end
        shuffle(edges)

        while len(edges_for_node) > 2:
            edge_start, edge_end = edges.pop()

            # Skip self edges
            if edge_start == edge_end:
                continue

            # Merge end node into start node
            for edge in edges_for_node[edge_end]:
                # Rename the edge
                for i in range(2):
                    if edge[i] == edge_end:
                        edge[i] = edge_start
            # move all edges from end node to start node
            edges_for_node[edge_start].extend(edges_for_node[edge_end])
            del edges_for_node[edge_end]

            # remove any self edges in start
            edges_for_node[edge_start] = [
                edge for edge in edges_for_node[edge_start] if edge[0] != edge[1]
            ]

            # update the nodesize
            nodesize[edge_start] += nodesize[edge_end]
            del nodesize[edge_end]

        return edges_for_node, nodesize

    @timeit
    @answer(49)
    def part_2(self) -> int:
        return 49

    def _parse_input(self):
        self.graph: dict[str, set] = defaultdict(set)
        for line in self.input:
            node, edges_list = line.split(": ")
            edges = edges_list.split()
            self.graph[node].update(edges)
