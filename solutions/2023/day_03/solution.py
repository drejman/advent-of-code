# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/3

from collections import defaultdict
from dataclasses import dataclass
from itertools import chain, groupby, product

from ...base import StrSplitSolution, answer


@dataclass
class Part:
    value: int
    line: int
    start: int
    end: int

    def __post_init__(self):
        if self.end < self.start:
            raise ValueError("Start and end set incorrectly")

    def is_symbol_adjacent(self, line: int, position: int) -> bool:
        if not (self.line - 1 <= line <= self.line + 1):
            return False
        if not (self.start - 1 <= position <= self.end + 1):
            return False
        return True


class Solution(StrSplitSolution):
    _year = 2023
    _day = 3

    @answer(538046)
    def part_1(self) -> int:
        self._parse_input()

        value = 0
        for part, shift in product(
            chain.from_iterable(self.parts.values()), [-1, 0, 1]
        ):
            if any(
                part.is_symbol_adjacent(line=part.line + shift, position=symbol)
                for symbol in self.symbols[part.line + shift]
            ):
                value += part.value
                continue
        return value

    @answer(81709807)
    def part_2(self) -> int:
        self._parse_input()

        gears = 0

        # get coordinates but only from lines where there are stars
        g = (
            (line_number, position)
            for line_number in self.stars.keys()
            for position in self.stars[line_number]
        )

        for line_number, position in g:
            parts_adjacent = 0
            current_gear_value = 1
            parts = (
                self.parts[line_number - 1]
                + self.parts[line_number]
                + self.parts[line_number + 1]
            )
            for part in parts:
                if part.is_symbol_adjacent(line=line_number, position=position):
                    parts_adjacent += 1
                    current_gear_value *= part.value
            else:
                if parts_adjacent >= 2:
                    gears += current_gear_value

        return gears

    def _parse_input(self):
        self.parts: dict[int, list[Part]] = defaultdict(list)
        self.symbols = defaultdict(list)
        self.stars = defaultdict(list)
        for line_number, line in enumerate(self.input):
            digits, symbols_, stars = self._parse_line(line)
            self.stars[line_number] = stars
            self.symbols[line_number] = symbols_

            # find groups of consecutive numbers
            for _, group in groupby(
                enumerate(digits.keys()), key=lambda x: x[0] - x[1]
            ):
                indices = [g[1] for g in group]
                self.parts[line_number].append(
                    Part(
                        value=int("".join(str(digits[ix]) for ix in indices)),
                        start=indices[0],
                        end=indices[-1],
                        line=line_number,
                    )
                )

    def _parse_line(self, line: str) -> tuple[dict[int, int], list[int], list[int]]:
        digits: dict[int, int] = {}
        symbols: list[int] = []
        stars: list[int] = []
        for ix, char in enumerate(line):
            match char:
                case ".":
                    continue
                case digit if digit.isdigit():
                    digits[ix] = int(digit)
                case "*":
                    stars.append(ix)
                case _:
                    symbols.append(ix)
        # stars still count as symbols for part 1
        symbols.extend(stars)
        return (digits, symbols, stars)
