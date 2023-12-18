# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/2


from dataclasses import astuple, dataclass, fields
from math import prod

from ...base import StrSplitSolution, answer, timeit


@dataclass
class Colors:
    red: int = 0
    green: int = 0
    blue: int = 0

    def __gt__(self, other):
        for a, b in zip(astuple(self), astuple(other)):
            if a > b:
                return True
        return False


class Solution(StrSplitSolution):
    _year = 2023
    _day = 2

    limit = Colors(red=12, green=13, blue=14)

    @timeit
    @answer(2593)
    def part_1(self) -> int:
        games = 0
        for line in self.input:
            game, sets = self._parse_input_line(line)
            for set_ in sets:
                if set_ > self.limit:
                    break
            else:
                games += game
        return games

    @timeit
    @answer(54699)
    def part_2(self) -> int:
        powers = 0
        for line in self.input:
            _, sets = self._parse_input_line(line=line)
            powers += prod(
                max([getattr(set_, field.name) for set_ in sets])
                for field in fields(Colors)
            )
        return powers

    @staticmethod
    def _parse_input_line(line: str) -> tuple[int, list[Colors]]:
        game_number, rest = line.split(":")
        game_number = int(game_number.removeprefix("Game "))
        results = []
        sets = rest.split(";")
        for set_ in sets:
            cubes = set_.split(",")
            colors = [cube.split() for cube in cubes]
            colors = {color[1]: int(color[0]) for color in colors}
            colors = Colors(**colors)
            results.append(colors)
        return (game_number, results)
