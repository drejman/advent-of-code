# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/15

from collections import OrderedDict, defaultdict
from functools import cache
from ...base import StrSplitSolution, answer, timeit


class Solution(StrSplitSolution):
    separator = ","
    _year = 2023
    _day = 15

    EQUAL = "="
    DASH = "-"

    @timeit
    @answer(503154)
    def part_1(self) -> int:
        return sum(self._hash(x) for x in self.input)

    @timeit
    @answer(251353)
    def part_2(self) -> int:
        self.boxes = defaultdict(OrderedDict)
        for sequence in self.input:
            if self.EQUAL in sequence:
                self._equals_sign(sequence)
            elif self.DASH in sequence:
                self._dash(sequence)
        self.debug(self.boxes)
        result = 0
        for box_number, box in self.boxes.items():
            for slot, focal_length in enumerate(box.values(), 1):
                result += (box_number + 1) * slot * focal_length
        return result

    def _equals_sign(self, sequence: str):
        label, focal_length = sequence.split(self.EQUAL)
        box = self._hash(label)
        self.boxes[box][label] = int(focal_length)

    def _dash(self, sequence: str):
        label = sequence.removesuffix(self.DASH)
        box = self._hash(label)
        self.boxes[box].pop(label, None)

    @staticmethod
    @cache
    def _hash(sequence: str) -> int:
        current_value = 0
        for char in sequence:
            current_value += ord(char)
            current_value *= 17
            current_value = current_value % 256
        return current_value

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
