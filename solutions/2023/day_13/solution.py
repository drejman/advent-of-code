# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/13

from ...base import StrSplitSolution, answer, timeit


class Solution(StrSplitSolution):
    _year = 2023
    _day = 13

    @timeit
    @answer(30535)
    def part_1(self) -> int:
        self._parse_input()
        solution = 0
        for block in self.blocks:
            current_solution = self._solve(block)
            self.debug(current_solution)
            solution += current_solution
        return solution

    @timeit
    @answer(30844)
    def part_2(self) -> int:
        self._parse_input()
        solution = 0
        for block in self.blocks:
            current_solution = self._solve(block, expected=1)
            self.debug(current_solution)
            solution += current_solution
        return solution

    def _parse_input(self):
        self.blocks = []
        block = []
        for line in self.input:
            if line == "":
                self.blocks.append(block)
                block = []
            else:
                block.append(line)
        else:
            self.blocks.append(block)

    def _solve(self, block: list[str], expected: int = 0) -> int:
        result = 0
        # horizontal line of symmetry:
        result += self._find_symmetry(block, expected) * 100

        # vertical line of symmetry:
        t_block = self._flip(block)
        self.debug(t_block)
        result += self._find_symmetry(t_block, expected)
        return result

    def _find_symmetry(self, block: list[str], expected: int = 0) -> int:
        result = 0
        for i in range(0, len(block) - 1):
            if (
                sum(
                    sum(
                        (
                            block[i + j + 1][k] != block[i - j][k]
                            for k in range(len(block[i]))
                        )
                    )
                    for j in range(0, min(i + 1, len(block) - i - 1))
                )
                == expected
            ):
                result += i + 1
        return result

    @staticmethod
    def _flip(block: list[str]) -> list[str]:
        return ["".join([line[i] for line in block]) for i in range(len(block[0]))]
