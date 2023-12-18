# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/18

from shapely import Polygon

from ...base import StrSplitSolution, answer, timeit


class Solution(StrSplitSolution):
    _year = 2023
    _day = 18

    @timeit
    @answer(61661)
    def part_1(self) -> int:
        self._parse_input()
        return self._get_lagoon_area(dig_plan=self._dig_plan)

    @timeit
    @answer(111131796939729)
    def part_2(self) -> int:
        self._parse_input(part=2)
        return self._get_lagoon_area(dig_plan=self._dig_plan)

    def _parse_input(self, part: int = 1):
        self._dig_plan = []
        directions = {0: "R", 1: "D", 2: "L", 3: "U"}
        for line in self.input:
            dir, length, color = line.split()
            color = color.removeprefix("(#").removesuffix(")")
            length = int(length)
            record = (
                (dir, length)
                if part == 1
                else (directions[int(color[5])], int(color[:5], 16))
            )
            self._dig_plan.append(record)

    @staticmethod
    def _get_lagoon_area(dig_plan: list[tuple[str, int]]) -> int:
        DIRS = {"U": (0, 1), "D": (0, -1), "R": (1, 0), "L": (-1, 0)}

        coords = (0, 0)
        path_ = [coords]
        for dir, length in dig_plan:
            shift = DIRS[dir]
            coords = (coords[0] + shift[0] * length, coords[1] + shift[1] * length)
            path_.append(coords)

        return int(Polygon(path_).buffer(0.5, join_style="mitre").area)
