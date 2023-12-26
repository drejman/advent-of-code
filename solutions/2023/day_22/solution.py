# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/22

from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass
from itertools import product
from typing import NamedTuple

from ...base import StrSplitSolution, answer, timeit


class Coordinates(NamedTuple):
    x: int
    y: int
    z: int


@dataclass
class Brick:
    p0: Coordinates
    p1: Coordinates
    _height: int | None = None

    def surface_projection(self):
        return [
            (x, y)
            for x, y in product(
                range(min(self.p0.x, self.p1.x), max(self.p0.x, self.p1.x) + 1),
                range(min(self.p0.y, self.p1.y), max(self.p0.y, self.p1.y) + 1),
            )
        ]

    @property
    def height(self) -> int:
        if self._height:
            return self._height
        self._height = abs(self.p0.z - self.p1.z) + 1
        return self._height

    @property
    def min_z(self) -> int:
        return min(self.p0.z, self.p1.z)


class Solution(StrSplitSolution):
    _year = 2023
    _day = 22

    @timeit
    @answer(482)
    def part_1(self) -> int:
        self._parse_input()
        self._bricks_fall()
        result = []
        for brick_num in self.bricks_contact.keys():
            if all(len(v) > 1 for v in self.bricks_contact.values() if brick_num in v):
                result.append(brick_num)
        return len(result)

    @timeit
    @answer(103010)
    def part_2(self) -> int:
        sum_total = 0
        for brick_num in self.bricks_contact.keys():
            bricks_contact = deepcopy(self.bricks_contact)
            # for each brick we start with analyzing whether it can be safely removed
            removed = {brick_num}
            q = deque([brick_num])
            while q:
                # analyze what will happen if brick is removed
                num = q.popleft()
                for brick in self.bricks_above[num]:
                    bricks_contact[brick].difference_update(removed)
                    if not bricks_contact[brick]:
                        removed.add(brick)
                        q.append(brick)
            sum_total += len(removed) - 1  # exclude the first brick (desintegrated one)
        return sum_total

    def _parse_input(self):
        self.bricks = []
        for line in self.input:
            first, second = line.split("~")
            self.bricks.append(
                Brick(
                    self._coordinates_from_input(first),
                    self._coordinates_from_input(second),
                )
            )
        self.bricks.sort(key=lambda brick: brick.min_z)

    @staticmethod
    def _coordinates_from_input(input_: str) -> Coordinates:
        return Coordinates(*map(int, input_.split(",")))

    def _bricks_fall(self):
        self.heights: dict[tuple[int, int], tuple[int, int]] = defaultdict(
            lambda: (0, 0)
        )
        self.bricks_contact: dict[int, set[int]] = {}
        self.bricks_above: dict[int, set[int]] = defaultdict(set)
        for num, brick in enumerate(self.bricks, 1):
            coordinates = brick.surface_projection()
            max_z = max(self.heights[coordinates][0] for coordinates in coordinates)
            self.bricks_contact[num] = set(
                self.heights[coordinates][1]
                for coordinates in coordinates
                if self.heights[coordinates][0] == max_z
                and self.heights[coordinates][1] != 0
            )
            for brick_num in self.bricks_contact[num]:
                self.bricks_above[brick_num].add(num)
            for coords in coordinates:
                self.heights[coords] = (max_z + brick.height, num)
