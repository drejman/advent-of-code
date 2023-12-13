# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/11
from itertools import combinations

from ...base import StrSplitSolution, answer, timeit


class Solution(StrSplitSolution):
    _year = 2023
    _day = 11

    @timeit
    @answer(9329143)
    def part_1(self) -> int:
        self._parse_input()
        sum_ = 0
        for g1, g2 in combinations(self.galaxies, r=2):
            sum_ += self._find_distance(g1, g2)
        return sum_

    def _find_distance(self, g1: tuple[int, int], g2: tuple[int, int]) -> int:
        dist = 0
        for i in range(min(g1[0], g2[0]), max(g1[0], g2[0])):
            dist += self.column_weights[i]
        for j in range(min(g1[1], g2[1]), max(g1[1], g2[1])):
            dist += self.row_weights[j]
        return dist

    @timeit
    @answer(710674907809)
    def part_2(self) -> int:
        self._parse_input(weight=1000000)
        sum_ = 0
        for g1, g2 in combinations(self.galaxies, r=2):
            sum_ += self._find_distance(g1, g2)
        return sum_

    def _parse_input(self, weight=2):
        # find empty lines
        galaxy = "#"
        self.row_weights = {}
        self.column_weights = {}
        self.galaxies = []
        self.columns = ["" for _ in range(len(self.input[0]))]

        for ix, line in enumerate(self.input):
            for jx, char in enumerate(line):
                self.columns[jx] += char
            index = line.find(galaxy)
            if index == -1:
                self.row_weights[ix] = weight
            else:
                self.row_weights[ix] = 1
            while index != -1:
                self.galaxies.append((index, ix))
                index = line.find(galaxy, index + 1)

        for ix, column in enumerate(self.columns):
            if galaxy not in column:
                self.column_weights[ix] = weight
            else:
                self.column_weights[ix] = 1

        self.debug(self.row_weights)
        self.debug(self.column_weights)
        self.debug(self.galaxies)

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
