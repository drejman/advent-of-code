# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/14

from functools import cache
from typing import Sequence

from ...base import StrSplitSolution, answer, timeit


class Solution(StrSplitSolution):
    _year = 2023
    _day = 14

    @timeit
    @answer(108935)
    def part_1(self) -> int:
        self.beams = tuple(self.input)
        self.beams = self._move(self.beams, direction="N")
        result = 0
        max_value = len(self.beams)
        for ln, line in enumerate(self.beams):
            result += len(list(x for x in line if x == "O")) * (max_value - ln)

        return result

    @timeit
    @answer(100876)
    def part_2(self) -> int:
        self.beams: tuple[str, ...] = tuple(self.input)
        self.previous_cycle_beams = {self.beams: 0}
        i = 0
        max_cycles = 1000000000
        while i < max_cycles:
            for dir in "NWSE":
                self.beams = self._move(self.beams, dir)
            i += 1
            if repeat := self.previous_cycle_beams.get(self.beams):
                period = i - repeat  # 1
                i += ((max_cycles - i) // period) * period
            self.previous_cycle_beams[self.beams] = i
        result = 0
        max_value = len(self.beams)
        for ln, line in enumerate(self.beams):
            result += len(list(x for x in line if x == "O")) * (max_value - ln)

        return result

    @classmethod
    @cache
    def _move(cls, beams: tuple[str, ...], direction: str) -> tuple[str, ...]:
        beams = tuple(cls._transform(beams, direction))

        new_beams = []
        new_beams.append(beams[0])
        for ln, line in enumerate(beams[1:], 1):
            mod_line = ""
            for ix, char in enumerate(line):
                if char == "O":
                    col = "".join(line[ix] for line in new_beams)
                    if (pos := max(col.rfind("O"), col.rfind("#"))) != -1:
                        if pos + 1 < ln and new_beams[pos + 1][ix] == ".":
                            new_beams[pos + 1] = (
                                new_beams[pos + 1][:ix]
                                + "O"
                                + new_beams[pos + 1][ix + 1 :]
                            )
                            mod_line += "."
                        else:
                            mod_line += "O"
                    elif col.startswith("."):
                        new_beams[0] = new_beams[0][:ix] + "O" + new_beams[0][ix + 1 :]
                        mod_line += "."
                    else:
                        mod_line += char
                else:
                    mod_line += char
            new_beams.append(mod_line)

        new_beams = tuple(cls._transform(new_beams, direction, True))
        return new_beams

    @staticmethod
    def _transpose(block: Sequence[str]) -> list[str]:
        return ["".join([line[i] for line in block]) for i in range(len(block[0]))]

    @classmethod
    def _transform(
        cls, block: Sequence[str], direction: str, revert: bool = False
    ) -> Sequence[str]:
        match direction, revert:
            case "W", _:
                block = cls._transpose(block=block)
            case "S", _:
                block = block[::-1]
            case "E", True:
                block = block[::-1]
                block = cls._transpose(block=block)
            case "E", False:
                block = cls._transpose(block=block)
                block = block[::-1]
        return block
