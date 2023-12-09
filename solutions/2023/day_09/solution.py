# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/9
from itertools import pairwise

from ...base import StrSplitSolution, answer, timeit


class Solution(StrSplitSolution):
    _year = 2023
    _day = 9

    @timeit
    @answer(1647269739)
    def part_1(self) -> int:
        self._parse_input()
        result = 0
        for seq in self.sequences:
            result += self._extrapolate_end(seq)[-1]
        return result

    @timeit
    @answer(864)
    def part_2(self) -> int:
        self._parse_input()
        result = 0
        for seq in self.sequences:
            result += self._extrapolate_beginning(seq)[0]
        return result

    @classmethod
    def _extrapolate_end(cls, seq: list[int]) -> list[int]:
        if all(x == 0 for x in seq):
            seq.append(0)
            return seq
        diffs = [pair[1] - pair[0] for pair in pairwise(seq)]
        derivative = cls._extrapolate_end(diffs)
        seq.append(seq[-1] + derivative[-1])
        return seq

    @classmethod
    def _extrapolate_beginning(cls, seq: list[int]) -> list[int]:
        if all(x == 0 for x in seq):
            seq.insert(0, 0)
            return seq
        diffs = [pair[1] - pair[0] for pair in pairwise(seq)]
        derivative = cls._extrapolate_beginning(diffs)
        seq.insert(0, seq[0] - derivative[0])
        return seq

    def _parse_input(self):
        self.sequences: list[list[int]] = [
            list(map(int, line.split())) for line in self.input
        ]
