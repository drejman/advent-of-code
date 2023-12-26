# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/23

from collections import deque
from copy import deepcopy

import networkx as nx

from ...base import StrSplitSolution, answer, timeit
from ...utils.coordinates import Coordinates


class Solution(StrSplitSolution):
    _year = 2023
    _day = 23
    DIRS = [
        Coordinates(0, 1),
        Coordinates(0, -1),
        Coordinates(1, 0),
        Coordinates(-1, 0),
    ]
    ALLOWED_CHARS = {DIRS[0]: "v", DIRS[1]: "^", DIRS[2]: ">", DIRS[3]: "<"}

    @timeit
    @answer(2282)
    def part_1(self) -> int:
        self._parse_input()
        paths = self.walk_paths()
        return (
            max(len(p) for p in paths) - 1
        )  # result is number of steps and not fields, therefore remove starting field

    @timeit
    @answer(6646)
    def part_2(self) -> int:
        self._parse_input()
        self.ALLOWED_CHARS = {
            self.DIRS[0]: "v^<>",
            self.DIRS[1]: "v^<>",
            self.DIRS[2]: "v^<>",
            self.DIRS[3]: "v^<>",
        }
        self.make_undirected_graph()
        sums = []
        for path in nx.all_simple_paths(self.graph, self._initial, self._final):
            total = nx.path_weight(self.graph, path, "weight")
            sums.append(total)
        return max(sums)

    def _parse_input(self):
        self._map: dict[Coordinates, str] = {}
        col, row = 0, 0
        for row, line in enumerate(self.input):
            for col, char in enumerate(line):
                self._map[Coordinates(col, row)] = char
                if char == "." and row == 0:
                    self._initial = Coordinates(col, row)
                if char == ".":
                    self._final = Coordinates(col, row)
        else:
            self._max_size = Coordinates(col, row)
        self._graph = []

    def walk_paths(self):
        q = deque()
        q.append(([self._initial], set()))
        finished = []
        while q:
            path, visited = q.pop()
            while True:
                current = path[-1]
                if current == self._final:
                    finished.append(path)
                    break
                visited.add(current)
                valid_coordinates = list(
                    current + dir
                    for dir in self.DIRS
                    if self._map.get(current + dir, "#")
                    in "." + self.ALLOWED_CHARS[dir]
                    and current + dir not in visited
                )
                if len(valid_coordinates) == 1:
                    path.append(valid_coordinates[0])
                elif len(valid_coordinates) > 1:
                    for vc in valid_coordinates:
                        q.append((path + [vc], deepcopy(visited)))
                    break
                else:
                    break
        return finished

    def make_directed_graph(self):
        graph = nx.DiGraph()
        nodes: deque[tuple[Coordinates | None, Coordinates, int]] = deque(
            [(self._initial, self._initial, 0)]
        )
        graph.add_node(self._initial)
        graph.add_node(self._final)
        visited = set()
        while nodes:
            previous, current, weight = nodes.popleft()
            visited.add(current)
            valid_coordinates = list(
                current + dir
                for dir in self.DIRS
                if self._map.get(current + dir, "#") in "." + self.ALLOWED_CHARS[dir]
            )
            allowed_coordinates = [vc for vc in valid_coordinates if vc not in visited]
            if current == self._final:
                graph.add_edge(previous, current, weight=weight)
            if len(allowed_coordinates) == 0:
                for vc in valid_coordinates:
                    if vc in graph.nodes:
                        graph.add_edge(previous, vc, weight=weight + 1)
            if len(allowed_coordinates) == 1:
                nodes.append((previous, allowed_coordinates[0], weight + 1))
            if len(allowed_coordinates) > 1:
                graph.add_node(current)
                graph.add_edge(previous, current, weight=weight)
                nodes.extend([(current, ac, 1) for ac in allowed_coordinates])
        self.digraph = graph

    def make_undirected_graph(self):
        graph = nx.Graph()

        nodes: deque[tuple[Coordinates | None, Coordinates]] = deque(
            [(None, self._initial)]
        )
        visited = set()
        weight = 0

        while nodes:
            previous, current = nodes.pop()
            if current in visited:
                if current in graph.nodes and previous != current:
                    graph.add_edge(previous, current, weight=weight + 1)
                    weight = 0
                continue
            visited.add(current)
            weight += 1
            valid_coordinates = list(
                current + dir
                for dir in self.DIRS
                if self._map.get(current + dir, "#") in "." + self.ALLOWED_CHARS[dir]
            )
            if len(valid_coordinates) == 1:
                if previous:
                    graph.add_edge(previous, current, weight=weight)
                graph.add_node(current)
                weight = 0
                nodes.extend([(current, vc) for vc in valid_coordinates])
            elif len(valid_coordinates) == 2:
                nodes.extend([(previous, vc) for vc in valid_coordinates])
            elif len(valid_coordinates) > 2:
                graph.add_node(current)
                graph.add_edge(previous, current, weight=weight)
                weight = 0
                nodes.extend([(current, vc) for vc in valid_coordinates])
        self.graph = graph
