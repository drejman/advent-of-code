# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/6

from math import sqrt
from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2023
    _day = 6

    @answer(131376)
    def part_1(self) -> int:
        self._parse_input()

        ways_total = 1
        for time, distance in zip(self.times, self.distances):
            ways = 0
            # brute force solution
            for i in range(time):
                if i*(time-i) > distance:
                    ways += 1
            ways_total *= ways
        
        return ways_total

    @answer(34123437)
    def part_2(self) -> int:
        self._parse_input()
        time = int("".join((str(x) for x in self.times)))
        distance = int("".join((str(x) for x in self.distances)))

        # quadratic equation solution
        # equation: -x^2 + time * x - distance = 0
        discriminant = time**2 -4*distance
        if discriminant < 0:
            raise ValueError(f"Discriminant negative: {discriminant}")
        sqrt_delta = sqrt(discriminant)
        x1 = (-1*time + sqrt_delta)/-2
        x2 = (-1*time - sqrt_delta)/-2
        return int(x2+1) - int(x1+1)

    def _parse_input(self):
        self.times: list[int] = list(map(int, self.input[0].removeprefix("Time:").split()))
        self.distances: list[int] = list(map(int, self.input[1].removeprefix("Distance:").split()))
