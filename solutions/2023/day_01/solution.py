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

    numbers = {'one': "1",
               'two': "2",
               'three': "3",
               'four': "4",
               'five': "5",
               'six': "6",
               'seven': "7",
               'eight': "8",
               'nine': "9",
               }

    @answer(54697)
    def part_1(self) -> int:
        numbers = []
        for line in self.input:
            self.debug(f"word: {line}")
            try:
                digits = self._find_all_digits(word=line)
            except ValueError:
                continue
            first_digit = digits[min(digits.keys())]
            last_digit = digits[max(digits.keys())]
            numbers.append(int(first_digit+last_digit))
        return sum(numbers)


    @staticmethod
    def _find_first_digit(word: str) -> str:
        for char in word:
            if char.isdigit():
                return char
        raise ValueError(f"No digits found in {word}")
    
    @staticmethod
    def _find_last_digit(word: str) -> str:
        for char in word[::-1]:
            if char.isdigit():
                return char
        raise ValueError(f"No digits found in {word}")
    
    @classmethod
    def _find_all_digits(cls, word: str, words_also: bool = False) -> dict[int, str]:
        digits = {}
        for ix, char in enumerate(word):
            if char.isdigit():
                digits[ix] = char
            if words_also:
                for number, value in cls.numbers.items():
                    if (index := word.find(number, ix, ix+5)) != -1:
                        digits[index] = value
        if not digits:
            raise ValueError(f"No digits found in {word}")
        return digits


    @answer(54885)
    def part_2(self) -> int:
        numbers = []
        for line in self.input:
            self.debug(f"word: {line}")
            try:
                digits = self._find_all_digits(word=line, words_also=True)
            except ValueError:
                continue
            first_digit = digits[min(digits.keys())]
            last_digit = digits[max(digits.keys())]
            numbers.append(int(first_digit+last_digit))
        return sum(numbers)

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
