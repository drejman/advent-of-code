# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/1
# As they're making the final adjustments, they discover that their calibration document (your puzzle input)
#  has been amended by a very young Elf who was apparently just excited to show off her art skills.
#  Consequently, the Elves are having trouble reading the values on the document.

# The newly-improved calibration document consists of lines of text;
# each line originally contained a specific calibration value that the Elves now need to recover.
# On each line, the calibration value can be found by combining the first digit and the last digit (in that order)
#  to form a single two-digit number.

# For example:

# 1abc2
# pqr3stu8vwx
# a1b2c3d4e5f
# treb7uchet

# In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

# Consider your entire calibration document. What is the sum of all of the calibration values?

from ...base import StrSplitSolution, answer


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

    @answer(54697)
    def part_1(self) -> int:
        return self.solve_part(words_also=False)

    @answer(54885)
    def part_2(self) -> int:
        return self.solve_part(words_also=True)

    def solve_part(self, words_also: bool):
        result = 0
        for line in self.input:
            self.debug(f"word: {line}")
            try:
                digits = self._find_all_digits(word=line, words_also=words_also)
            except ValueError:
                continue
            first_digit = digits[min(digits.keys())]
            last_digit = digits[max(digits.keys())]
            result += int(first_digit + last_digit)
        return result

    @classmethod
    def _find_all_digits(cls, word: str, words_also: bool = False) -> dict[int, str]:
        digits = {}
        numbers = cls.numbers.copy()
        if words_also:
            numbers.update(cls.words)
        for ix, _ in enumerate(word):
            for number, value in numbers.items():
                if (index := word.find(number, ix, ix + cls.window)) != -1:
                    digits[index] = value
        if not digits:
            raise ValueError(f"No digits found in {word}")
        return digits
