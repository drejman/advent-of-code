# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/7
from collections import Counter
from string import digits

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2023
    _day = 7

    @answer(250370104)
    def part_1(self) -> int:
        self._parse_input()
        self.game.sort(key=lambda x: self._sort_hand_part1(x[0]))
        self.debug(self.game)
        return self._get_result()

    @answer(251735672)
    def part_2(self) -> int:
        self._parse_input()
        self.game.sort(key=lambda x: self._sort_hand_part2(x[0]))
        self.debug(self.game)
        return self._get_result()

    def _get_result(self):
        result = 0
        for ix, (hand, bid) in enumerate(self.game):
            self.debug(f"{ix+1} {hand} {bid}")
            result += (ix+1)*bid
        return result

    def _parse_input(self):
        self.game: list[tuple[str, int]] = []
        for line in self.input:
            hand, bid = line.split()
            self.game.append((hand, int(bid)))

    @staticmethod
    def _sort_hand_part1(hand: str) -> int:
        cards = digits+"TJQKA"
        counter = Counter(hand)
        counts = list(sorted(counter.values(), reverse=True))
        counts.append(0)  # hack to get rid of IndexErrors
        rank = counts[0]*10+counts[1]

        score = 0
        levels = len(hand)
        for ix, card in enumerate(hand):
            score += cards.index(card) * (100**(levels-ix))
        score += rank * (100**(levels+1))
        return score

    @staticmethod
    def _sort_hand_part2(hand: str) -> int:
        cards = "J"+digits+"TQKA"
        score = 0
        levels = len(hand)
        for ix, card in enumerate(hand):
            score += cards.index(card) * (100**(levels-ix))

        counter = Counter((card for card in hand if card != "J"))
        counts = list(sorted(counter.values(), reverse=True))
        counts.extend([0, 0])  # hack to get rid of IndexErrors
        for _ in (card for card in hand if card == "J"):
            if counts[0] < 5:
                counts[0] += 1
        rank = counts[0]*10+counts[1]
        score += rank * (100**(levels+1))
        return score
