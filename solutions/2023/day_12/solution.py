# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/12
from functools import cache
from itertools import groupby, product

from ...base import StrSplitSolution, answer, timeit


class Solution(StrSplitSolution):
    _year = 2023
    _day = 12

    BROKEN = "#"
    WORKING = "."
    UNKNOWN = "?"

    @timeit
    @answer(7032)
    def part_1(self) -> int:
        solutions = 0
        for line in self.input:
            solution_dp = self._solve_dp(line)
            # solution_bf = self._solve(line)
            # if solution_bf != solution_dp:
            #     print(line, solution_dp, solution_bf)
            #     break
            solutions += solution_dp
        return solutions

    @timeit
    @answer(1493340882140)
    def part_2(self) -> int:
        solutions = 0
        for line in self.input:
            solution_dp = self._solve_dp_p2(line)
            solutions += solution_dp
        return solutions

    def _solve(self, line: str) -> int:
        solutions = 0

        springs, numbers = line.split()
        numbers = list(map(int, numbers.split(",")))
        unknown = springs.count(self.UNKNOWN)
        # self.debug(unknown)
        # possibilities = [self.BROKEN if x%2==0 else self.WORKING for x in range(unknown*2)]
        # self.debug(possibilities)
        for comb_ in product([self.BROKEN, self.WORKING], repeat=unknown):
            # self.debug(comb_)
            new_springs = springs
            for i in range(unknown):
                new_springs = new_springs.replace(self.UNKNOWN, comb_[i], 1)
            # self.debug(new_springs)
            lengths = [
                len(list(k)) for g, k in groupby(new_springs) if g == self.BROKEN
            ]
            if lengths == numbers:
                solutions += 1

        return solutions

    def _solve_dp(self, line: str) -> int:
        solutions = 0

        springs, numbers = line.split()
        damaged = tuple(map(int, numbers.split(",")))
        solutions = self._get_solutions(springs, damaged)
        return solutions

    def _solve_dp_p2(self, line: str) -> int:
        solutions = 0

        springs, numbers = line.split()
        numbers = ",".join([numbers] * 5)
        springs = "?".join([springs] * 5)
        damaged = tuple(map(int, numbers.split(",")))
        solutions = self._get_solutions(springs, damaged)
        return solutions

    @cache
    def _get_solutions(self, springs: str, damaged: tuple[int, ...]) -> int:
        if len(damaged) == 0:
            if self.BROKEN not in springs:
                return 1
            return 0
        if sum(damaged) > len(springs):
            return 0
        # self.debug(f"{springs}: {damaged}")
        # if there are no ? then go straight to answer
        if self.UNKNOWN not in springs:
            lengths = tuple(
                len(list(k)) for g, k in groupby(springs) if g == self.BROKEN
            )
            if lengths == damaged:
                return 1
            return 0

        # if starts with ? then split into two branches
        if springs[0] == self.UNKNOWN:
            solutions = self._get_solutions(
                springs=springs.replace(self.UNKNOWN, self.BROKEN, 1), damaged=damaged
            ) + self._get_solutions(
                springs=springs.replace(self.UNKNOWN, self.WORKING, 1), damaged=damaged
            )
            if solutions:
                self.debug(f"{springs}: {damaged} solutions: {solutions}")
            return solutions

        groups = [
            (g, len(list(k))) for ix, (g, k) in enumerate(groupby(springs)) if ix < 2
        ]

        # if starts with . than remove whole group and continue
        if groups[0][0] == self.WORKING:
            index = groups[0][1]
            return self._get_solutions(springs=springs[index:], damaged=damaged)

        # if starts with #
        if groups[0][0] == self.BROKEN:
            if groups[0][1] > damaged[0]:
                return 0
            # if # group end is known check match, remove groups and continue
            if groups[1][0] == self.WORKING:
                if groups[0][1] == damaged[0]:
                    index = groups[0][1] + groups[1][1]
                    return self._get_solutions(
                        springs=springs[index:], damaged=damaged[1:]
                    )
                return 0

            # if # group could be elongated by ? split
            if groups[1][0] == self.UNKNOWN:
                solutions = self._get_solutions(
                    springs=springs.replace(self.UNKNOWN, self.BROKEN, 1),
                    damaged=damaged,
                ) + self._get_solutions(
                    springs=springs.replace(self.UNKNOWN, self.WORKING, 1),
                    damaged=damaged,
                )
                if solutions:
                    self.debug(f"{springs}: {damaged} solutions: {solutions} ")
                return solutions
        raise ValueError(f"Nothing matched for {springs}: {damaged}")

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
