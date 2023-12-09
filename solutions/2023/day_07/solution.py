# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/7
from collections import Counter
from string import digits
from typing import Callable

from ...base import StrSplitSolution, answer, timeit


class Solution(StrSplitSolution):
    _year = 2023
    _day = 7

    @timeit
    @answer(250370104)
    def part_1(self) -> int:
        self._parse_input()
        self.game.sort(key=lambda x: self._sort_hand_part1(x[0]))
        return self._get_result()

    @timeit
    @answer(251735672)
    def part_2(self) -> int:
        self._parse_input()
        self.game.sort(key=lambda x: self._sort_hand_part2(x[0]))
        return self._get_result()

    def _get_result(self):
        result = 0
        for ix, (hand, bid) in enumerate(self.game):
            result += (ix + 1) * bid
        return result

    def _parse_input(self):
        self.game: list[tuple[str, int]] = []
        for line in self.input:
            hand, bid = line.split()
            self.game.append((hand, int(bid)))

    @classmethod
    def _sort_hand_part1(cls, hand: str) -> int:
        cards = digits + "TJQKA"
        func = cls._sort_template_method(cards_order=cards)
        return func(hand)

    @classmethod
    def _sort_hand_part2(cls, hand: str) -> int:
        cards = "J" + digits + "TQKA"
        func = cls._sort_template_method(cards_order=cards, jokers="J")
        return func(hand)

    @staticmethod
    def _sort_template_method(
        cards_order: str, jokers: str = ""
    ) -> Callable[[str], int]:
        def _sort(hand: str) -> int:
            # start with finding type (four-of-kind etc)
            # based on two cards (because of full house) with highest count
            counter = Counter((card for card in hand if card not in jokers))
            counts = list(sorted(counter.values(), reverse=True))
            counts.extend([0] * (len(jokers) + 1))  # hack to get rid of IndexErrors
            # jokers are treated as cards of highest count (always most beneficial)
            for _ in (card for card in hand if card in jokers):
                counts[0] += 1
            # type of hand has highest impact so is multiplied by highiest factor
            type_score = counts[0] * 10 + counts[1]
            levels = len(hand)
            score = type_score * (100 ** (levels + 1))

            # last part of score is highest card
            # starting from the left (highest factor) to the right (lowest factor)
            for ix, card in enumerate(hand):
                score += cards_order.index(card) * (100 ** (levels - ix))
            return score

        return _sort
