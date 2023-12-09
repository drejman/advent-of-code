# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/8
from itertools import chain, cycle
from math import lcm

from ...base import StrSplitSolution, answer, timeit


class Solution(StrSplitSolution):
    _year = 2023
    _day = 8

    @timeit
    @answer(16343)
    def part_1(self) -> int:
        self._parse_input()
        self.debug(self.mapping)
        current_location = "AAA"
        for ix, move in enumerate(cycle(self.moves)):
            match move:
                case "L":
                    current_location = self.mapping[current_location][0]
                case "R":
                    current_location = self.mapping[current_location][1]
            if current_location == "ZZZ":
                return ix + 1
        else:
            raise ValueError("No solution found")

    @timeit
    @answer(15299095336639)
    def part_2(self) -> int:
        self._parse_input()

        current_locations = {
            key: key for key in self.mapping.keys() if key.endswith("A")
        }
        results = {k: [] for k in current_locations.keys()}

        for ix, move in enumerate(cycle(self.moves)):
            to_remove = []

            for initial, current in current_locations.items():
                if current.endswith("Z"):
                    results[initial].append(ix)
                    to_remove.append(initial)
                match move:
                    case "L":
                        current_locations[initial] = self.mapping[current][0]
                    case "R":
                        current_locations[initial] = self.mapping[current][1]
                current = current_locations[initial]

            for r in to_remove:
                current_locations.pop(r, None)

            if not current_locations:
                break
        return lcm(*[x for x in chain.from_iterable(results.values())])

    def _parse_input(self):
        self.moves = self.input[0].strip()
        self.mapping: dict[str, tuple[str, str]] = {}
        for line in self.input[2:]:
            key, values = line.split("=")
            v1, v2 = values.removeprefix(" (").removesuffix(")").split(",")
            self.mapping[key.strip()] = (v1, v2.lstrip())
