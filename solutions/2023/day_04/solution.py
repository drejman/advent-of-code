# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/4

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2023
    _day = 4

    @answer(26914)
    def part_1(self) -> int:
        self.numbers: dict[int, tuple[set[int], set[int]]] = {}
        self._parse_input()

        result = 0
        for card in self.numbers.keys():
            match = self.numbers[card][1].intersection(self.numbers[card][0])
            if match:
                result += 2 ** (len(match) - 1)
        return result

    # @answer(1234)
    def part_2(self) -> int:
        self.numbers: dict[int, tuple[set[int], set[int]]] = {}
        self._parse_input()

        results: dict[int, int] = {}
        cards: dict[int, int] = {}
        for card_number in sorted(self.numbers.keys()):
            match = self.numbers[card_number][1].intersection(
                self.numbers[card_number][0]
            )
            cards[card_number] = 1
            if match:
                results[card_number] = len(match)

        self.debug(results)
        for card_number in sorted(results.keys()):
            for i in range(1, results[card_number] + 1):
                try:
                    cards[card_number + i] += cards[card_number]
                except KeyError:
                    continue

        self.debug(cards)
        return sum(cards.values())

    def _parse_input(self) -> None:
        for line in self.input:
            card, numbers = line.split(":")
            card_number = int(card.removeprefix("Card "))
            winning_numbers, chosen_numbers = map(self._map, numbers.split("|"))
            self.numbers[card_number] = (winning_numbers, chosen_numbers)
        # self.debug(self.numbers)

    @staticmethod
    def _map(numbers: str) -> set[int]:
        numbers = numbers.replace("  ", " ").lstrip().strip()
        return set(map(int, numbers.split(" ")))

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
