# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/2
# You're launched high into the atmosphere!
# The apex of your trajectory just barely reaches the surface of a large island floating in the sky.
#  You gently land in a fluffy pile of leaves. It's quite cold, but you don't see much snow. An Elf runs over to greet you.

# The Elf explains that you've arrived at Snow Island and apologizes for the lack of snow.
#  He'll be happy to explain the situation, but it's a bit of a walk, so you have some time.
#  They don't get many visitors up here; would you like to play a game in the meantime?

# As you walk, the Elf shows you a small bag and some cubes which are either red, green, or blue.
# Each time you play this game, he will hide a secret number of cubes of each color in the bag,
#  and your goal is to figure out information about the number of cubes.

# To get information, once a bag has been loaded with cubes, the Elf will reach into the bag,
# grab a handful of random cubes, show them to you, and then put them back in the bag. He'll do this a few times per game.

# You play several games and record the information from each game (your puzzle input).
#  Each game is listed with its ID number (like the 11 in Game 11: ...)
# followed by a semicolon-separated list of subsets of cubes that were revealed from the bag (like 3 red, 5 green, 4 blue).

# For example, the record of a few games might look like this:

# Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
# Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
# Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
# Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

# In game 1, three sets of cubes are revealed from the bag (and then put back again).
# The first set is 3 blue cubes and 4 red cubes;
#  the second set is 1 red cube, 2 green cubes, and 6 blue cubes;
#  the third set is only 2 green cubes.

# The Elf would first like to know which games would have been
#  if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

# In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded with that configuration.
# However, game 3 would have been impossible because at one point the Elf showed you 20 red cubes at once;
# similarly, game 4 would also have been impossible because the Elf showed you 15 blue cubes at once.
#  If you add up the IDs of the games that would have been possible, you get 8.

# Determine which games would have been possible if the bag had been loaded with only 12 red cubes,
#  13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?

from dataclasses import astuple, dataclass, fields
from math import prod

from ...base import StrSplitSolution, answer


@dataclass
class Colors:
    red: int = 0
    green: int = 0
    blue: int = 0

    def __gt__(self, other):
        for a, b in zip(astuple(self), astuple(other)):
            if a > b:
                return True
        return False


class Solution(StrSplitSolution):
    _year = 2023
    _day = 2

    limit = Colors(red=12, green=13, blue=14)

    @answer(2593)
    def part_1(self) -> int:
        games = 0
        for line in self.input:
            game, sets = self._parse_input_line(line)
            for set_ in sets:
                if set_ > self.limit:
                    break
            else:
                games += game
        return games

    # @answer(1234)
    def part_2(self) -> int:
        powers = 0
        for line in self.input:
            game, sets = self._parse_input_line(line=line)
            powers += prod(
                max([getattr(set_, field.name) for set_ in sets])
                for field in fields(Colors)
            )
            self.debug(f"{game} {powers}")
        return powers

    @staticmethod
    def _parse_input_line(line: str) -> tuple[int, list[Colors]]:
        game_number, rest = line.split(":")
        game_number = int(game_number.removeprefix("Game "))
        results = []
        sets = rest.split(";")
        for set_ in sets:
            cubes = set_.split(",")
            colors = [cube.lstrip().strip().split(" ") for cube in cubes]
            colors = {color[1]: int(color[0]) for color in colors}
            colors = Colors(**colors)
            results.append(colors)
        return (game_number, results)

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
