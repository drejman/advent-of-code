# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/17
from collections import defaultdict
from copy import deepcopy
from functools import cache
from itertools import product
from math import inf
from typing import NamedTuple

from ...base import StrSplitSolution, answer, timeit

class Vertex(NamedTuple):
    col: int
    row: int
    dir: str  # allowed direction
    step: int  # allowed step

class Solution(StrSplitSolution):
    _year = 2023
    _day = 17

    @timeit
    # @answer(1234)
    def part_1(self) -> int:
        self._parse_input()
        self._dijkstra()
        # self.debug({k: v for k, v in self._distances.items() if k.row == 12 and k.col == 12})
        # self.debug(self._paths[Vertex(12, 12, "D", 3)])
        return min(v for k, v in self._distances.items() if (k.col, k.row) == self._max_size)
        # self.debug(self._distances)

    @timeit
    # @answer(1234)
    def part_2(self) -> int:
        pass


    def _parse_input(self):
        self._values: dict[tuple[int, int], int] = {}
        for row, line in enumerate(self.input):
            for col, char in enumerate(line):
                self._values[(col, row)] = int(char)
        else:
            self._max_size = (col, row)

    def _dijkstra(self, starting_node = (0, 0), max_step = 3):
        self._distances: dict[Vertex, int] = {Vertex(col=coord[0], row=coord[1], dir=step_dir, step=step_len): inf
                           for coord, step_dir, step_len in product(self._values.keys(), "UDLR", range(1,max_step+1))
                           if coord != starting_node}
        current_node = Vertex(col=starting_node[0], row=starting_node[1], dir="R", step=3)
        self._distances.update({current_node: 0,
                                Vertex(col=starting_node[0], row=starting_node[1], dir="D", step=3): 0})
        self._visited = {k: False for k in self._distances.keys()}
        # self._paths = {k: [] for k in self._distances.keys()}

        while True:
            unvisited_neighbors = [node for node, visited in self._visited.items() 
                                      if visited is False 
                                      and self._step_allowed(current_node, node)]
            # self.debug(current_node)
            # self.debug(unvisited_neighbors)
            # input()
            for neighbor in unvisited_neighbors :
                match current_node.dir:
                    case "R":
                        distance = sum(self._values[(col, current_node.row)] for col in range(current_node.col + 1, neighbor.col + 1)) + self._distances[current_node]
                    case "L":
                        distance = sum(self._values[(col, current_node.row)] for col in range(current_node.col - 1, neighbor.col - 1, -1))  + self._distances[current_node]
                    case "D":
                        distance = sum(self._values[(current_node.col, row)] for row in range(current_node.row + 1, neighbor.row + 1)) + self._distances[current_node]
                    case "U":
                        distance = sum(self._values[(current_node.col, row)] for row in range(current_node.row - 1, neighbor.row - 1, -1)) + self._distances[current_node]
                    case _:
                        distance = inf
                if distance < self._distances[neighbor]:
                    self._distances[neighbor] = distance
                    # self._paths[neighbor] = deepcopy(self._paths[current_node])+[current_node]
            self._visited[current_node] = True
            if all(v for k, v in self._visited.items() if (k.col, k.row) == self._max_size):
                break
            if all(self._visited.values()):
                break
            current_node = min({k: v for k,v in self._distances.items() if not self._visited[k]}, key=self._distances.get)
            if self._distances[current_node] == inf:
                break
            # self.debug(current_node)
            # input()
        # self.debug([(k,v) for k, v in self._distances.items() if v != inf])

    @staticmethod
    def _step_allowed(start_node: Vertex, dest_node: Vertex) -> bool:
        match start_node.dir:
            case "R":
                dist = dest_node.col - start_node.col
                if 0 < dist <= start_node.step and dest_node.row == start_node.row:
                    if dest_node.dir in "UD" or (dest_node.dir == "R" and (dist + dest_node.step) == start_node.step):
                        return True
            case "L":
                dist = start_node.col - dest_node.col
                if 0 < dist <= start_node.step and dest_node.row == start_node.row:
                    if dest_node.dir in "UD" or (dest_node.dir == "L" and (dist + dest_node.step) == start_node.step):
                        return True
            case "D":
                dist = dest_node.row - start_node.row
                if 0 < dist <= start_node.step and dest_node.col == start_node.col:
                    if dest_node.dir in "LR" or (dest_node.dir == "D" and (dist + dest_node.step) == start_node.step):
                        return True
            case "U":
                dist = start_node.row - dest_node.row
                if 0 < dist <= start_node.step and dest_node.col == start_node.col:
                    if dest_node.dir in "LR" or (dest_node.dir == "U" and (dist + dest_node.step) == start_node.step):
                        return True
        return False
