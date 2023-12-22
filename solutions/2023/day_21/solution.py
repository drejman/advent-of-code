# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/21
from functools import cache
from typing import NamedTuple, Self
from ...base import StrSplitSolution, answer, timeit

class Coordinates(NamedTuple):
    col: int
    row: int

    def __add__(self, other: Self) -> Self:
        return type(self)(col=self.col+other.col, row=self.row+other.row)

class Solution(StrSplitSolution):
    _year = 2023
    _day = 21
    DIRS = [Coordinates(1, 0), Coordinates(0, 1), Coordinates(-1, 0), Coordinates(0, -1)]
    STEPS = 64

    @timeit
    @answer(3572)
    def part_1(self) -> int:
        steps = self.STEPS
        if self.use_test_data:
            steps = 6

        self._parse_input()

        return self._calculate_steps(steps=steps)[steps]
        
    @timeit
    @answer(594606492802848)
    def part_2(self) -> int:
        self._parse_input()
        dim = self._max_size.row + 1
        steps = self.STEPS + 1
        if self.use_test_data:
            steps = 6

        result = self._calculate_steps(steps=steps+2*dim)
        # geometric progression based on sum of n terms of arithmetic sequence
        a0 = result[steps]
        a1 = result[steps+dim]
        a2 = result[steps+dim*2]

        b0 = a0
        b1 = a1-a0
        b2 = a2-a1
        n = 26501365 // dim
        return b0 + b1*n + (n*(n-1)//2)*(b2-b1)

    def _parse_input(self):
        self._map: dict[Coordinates, bool] = {}
        col, row = 0, 0
        for row, line in enumerate(self.input):
            for col, char in enumerate(line):
                self._map[Coordinates(col, row)] = False if char == "#" else True
                if char == "S":
                    self._initial = Coordinates(col, row)
        else:
            self._max_size = Coordinates(col, row)

    @cache
    def _is_inside_grid(self, coordinates: Coordinates):
        return 0 <= coordinates.col <= self._max_size[0] and 0 <= coordinates.row <= self._max_size[1]
    
    @cache
    def _get_map_coordinates(self, coordinates: Coordinates) -> Coordinates:
        if self._is_inside_grid(coordinates):
            return coordinates
        return Coordinates(col=(coordinates.col % (self._max_size.col+1)), row=(coordinates.row % (self._max_size.row+1)))

    def _calculate_steps(self, steps: int):
        result = []
        _even_steps = {}
        _even_steps[self._initial] = True

        for i in range(int((steps+1)/2)):
            step_result = 0
            _odd_steps = {}
            for k, v in _even_steps.items():
                if v is True:
                    step_result += 1
                    for dir in self.DIRS:
                        new_coordinates = k+dir
                        if self._map[self._get_map_coordinates(new_coordinates)]:
                            _odd_steps[new_coordinates] = True
            result.append(step_result)

            step_result = 0
            _even_steps = {}
            for k, v in _odd_steps.items():
                if v is True:
                    step_result += 1
                    for dir in self.DIRS:
                        new_coordinates = k+dir
                        if self._map[self._get_map_coordinates(new_coordinates)]:
                            _even_steps[new_coordinates] = True
            result.append(step_result)

        result.append(len({k: v for k, v in _even_steps.items() if v is True}))
        return result