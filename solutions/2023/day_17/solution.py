# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/17
from functools import cache
from heapq import heappop, heappush
from typing import NamedTuple

from ...base import StrSplitSolution, answer, timeit


class Node(NamedTuple):
    col: int
    row: int
    blocked_dirs: str  # blocked directions


INF = int(1e9)


class Solution(StrSplitSolution):
    _year = 2023
    _day = 17
    DIRS = {"D": (0, 1), "R": (1, 0), "U": (0, -1), "L": (-1, 0)}
    BLOCKED_DIRS = {"D": "UD", "R": "RL", "U": "UD", "L": "LR"}

    @timeit
    @answer(694)
    def part_1(self) -> int:
        self._parse_input()
        return self._dijkstra()

    @timeit
    @answer(829)
    def part_2(self) -> int:
        self._parse_input()
        return self._dijkstra(min_step=4, max_step=10)

    def _parse_input(self):
        self._values: dict[tuple[int, int], int] = {}
        col, row = 0, 0
        for row, line in enumerate(self.input):
            for col, char in enumerate(line):
                self._values[(col, row)] = int(char)
        else:
            self._max_size = (col, row)

    def _dijkstra(self, max_step=3, min_step=1):
        self._nodes = []
        heappush(self._nodes, (0, Node(col=0, row=0, blocked_dirs="UD")))
        heappush(self._nodes, (0, Node(col=0, row=0, blocked_dirs="LR")))
        self._visited: set[Node] = set()
        self._costs: dict[Node, int] = {}

        while self._nodes:
            # get node
            cost, current_node = heappop(self._nodes)

            # check exit conditions
            if (current_node.col, current_node.row) == self._max_size:
                return cost
            if current_node in self._visited:
                continue

            # try every allowed direction
            for dir in "DURL":
                if dir in current_node.blocked_dirs:
                    continue
                cost_delta = 0

                # try every allowed distance
                for distance in range(1, max_step + 1):
                    col = current_node.col + self.DIRS[dir][0] * distance
                    row = current_node.row + self.DIRS[dir][1] * distance

                    # move to different direction if outside grid
                    if not self._is_inside_grid(col, row):
                        break

                    # increase cost but skip nodes below minimum step length
                    cost_delta += self._values[(col, row)]
                    if distance < min_step:
                        continue

                    new_cost = cost + cost_delta
                    # because we move max allowed distance in single direction then we can change directions every iteration
                    node = Node(col, row, self.BLOCKED_DIRS[dir])
                    if new_cost > self._costs.get(node, INF):
                        continue

                    self._costs[node] = new_cost
                    heappush(self._nodes, (new_cost, node))
            else:
                self._visited.add(current_node)
        else:
            raise ValueError("Solution not found")

    @cache
    def _is_inside_grid(self, col, row):
        return 0 <= col <= self._max_size[0] and 0 <= row <= self._max_size[1]
