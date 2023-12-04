# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/4

from collections import defaultdict

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2023
    _day = 4

    @answer(26914)
    def part_1(self) -> int:
        self._parse_input()

        result = 0
        for matches in filter(lambda x: x != 0, self.cards.values()):
            result += 2 ** (matches - 1)
        return result

    @answer(13080971)
    def part_2(self) -> int:
        self._parse_input()

        cards_won: dict[int, int] = defaultdict(int)
        last_card = max(self.cards.keys())
        for card_number, matches in self.cards.items():
            cards_won[card_number] += 1  # increment for original card

            # increment next N cards (N being number of matches) by number of copies of currectly processed card
            for i in range(
                card_number + 1, min(card_number + matches + 1, last_card + 1)
            ):
                cards_won[i] += cards_won[card_number]

        return sum(cards_won.values())

    def _parse_input(self) -> None:
        # represent input as a dict structure: {card_number: number_of_matches}
        self.cards: dict[int, int] = {}
        for line in self.input:
            card, numbers = line.split(":")
            card_number = int(card.removeprefix("Card "))
            winning_numbers, chosen_numbers = map(
                self._parse_numbers_part, numbers.split("|")
            )
            self.cards[card_number] = len(
                set(chosen_numbers).intersection(set(winning_numbers))
            )

    @staticmethod
    def _parse_numbers_part(numbers: str) -> set[int]:
        numbers = numbers.replace("  ", " ").lstrip().strip()
        return set(map(int, numbers.split(" ")))
