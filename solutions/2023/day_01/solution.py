# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/1

from ...base import StrSplitSolution, answer, timeit


class Solution(StrSplitSolution):
    _year = 2023
    _day = 1

    words = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    numbers = {
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
    }
    window = max([len(key) for key in words.keys()])

    @timeit
    @answer(54697)
    def part_1(self) -> int:
        return self.solve_part(words_also=False)

    @timeit
    @answer(54885)
    def part_2(self) -> int:
        return self.solve_part(words_also=True)

    def solve_part(self, words_also: bool):
        result = 0
        for line in self.input:
            digits = self._find_all_digits(word=line, words_also=words_also)
            if not digits:
                continue
            values = sorted(digits.keys())
            first, last = digits[values[0]], digits[values[-1]]
            result += int(first + last)
        return result

    @classmethod
    def _find_all_digits(cls, word: str, words_also: bool = False) -> dict[int, str]:
        digits = {}
        numbers = cls.numbers.copy()
        if words_also:
            numbers.update(cls.words)
        for ix in range(len(word)):
            for number, value in numbers.items():
                if (index := word.find(number, ix, ix + cls.window)) != -1:
                    digits[index] = value
        return digits
