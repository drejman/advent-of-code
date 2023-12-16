# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/16

from copy import deepcopy
from uuid import uuid4

from more_itertools import ilen

from ...base import StrSplitSolution, answer, timeit


class Beam:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    def __init__(
        self,
        direction: str,
        coordinates: tuple[int, int],
        fields: dict,
        beams: dict[tuple[int, int], list],
    ):
        self.id = uuid4()
        self.direction = direction
        self.coordinates = coordinates
        self.fields = fields
        self.beams = beams
        self.beams.get(coordinates, []).append(self.direction)

    def propagate(self):
        while True:
            next_coordinates = self._calculate_next_field()
            if not (next_field := self.fields.get(next_coordinates)):
                return
            if self.direction in self.beams[next_coordinates]:
                return
            match next_field, self.direction:
                case "|", (self.LEFT | self.RIGHT):
                    Beam(
                        direction=self.UP,
                        coordinates=next_coordinates,
                        fields=self.fields,
                        beams=self.beams,
                    ).propagate()
                    Beam(
                        direction=self.DOWN,
                        coordinates=next_coordinates,
                        fields=self.fields,
                        beams=self.beams,
                    ).propagate()
                    return
                case "-", (self.UP | self.DOWN):
                    Beam(
                        direction=self.LEFT,
                        coordinates=next_coordinates,
                        fields=self.fields,
                        beams=self.beams,
                    ).propagate()
                    Beam(
                        direction=self.RIGHT,
                        coordinates=next_coordinates,
                        fields=self.fields,
                        beams=self.beams,
                    ).propagate()
                    return
                case "\\", self.LEFT:
                    self.coordinates = next_coordinates
                    self.beams[next_coordinates].append(self.direction)
                    self.direction = self.UP
                case "\\", self.DOWN:
                    self.coordinates = next_coordinates
                    self.beams[next_coordinates].append(self.direction)
                    self.direction = self.RIGHT
                case "\\", self.RIGHT:
                    self.coordinates = next_coordinates
                    self.beams[next_coordinates].append(self.direction)
                    self.direction = self.DOWN
                case "\\", self.UP:
                    self.coordinates = next_coordinates
                    self.beams[next_coordinates].append(self.direction)
                    self.direction = self.LEFT
                case "/", self.LEFT:
                    self.coordinates = next_coordinates
                    self.beams[next_coordinates].append(self.direction)
                    self.direction = self.DOWN
                case "/", self.DOWN:
                    self.coordinates = next_coordinates
                    self.beams[next_coordinates].append(self.direction)
                    self.direction = self.LEFT
                case "/", self.RIGHT:
                    self.coordinates = next_coordinates
                    self.beams[next_coordinates].append(self.direction)
                    self.direction = self.UP
                case "/", self.UP:
                    self.coordinates = next_coordinates
                    self.beams[next_coordinates].append(self.direction)
                    self.direction = self.RIGHT
                case _, _:
                    self.coordinates = next_coordinates
                    self.beams[next_coordinates].append(self.direction)

    def _calculate_next_field(self) -> tuple[int, int]:
        match self.direction:
            case self.UP:
                return (self.coordinates[0], self.coordinates[1] - 1)
            case self.DOWN:
                return (self.coordinates[0], self.coordinates[1] + 1)
            case self.LEFT:
                return (self.coordinates[0] - 1, self.coordinates[1])
            case self.RIGHT:
                return (self.coordinates[0] + 1, self.coordinates[1])
        raise ValueError


class Solution(StrSplitSolution):
    _year = 2023
    _day = 16

    @timeit
    @answer(7242)
    def part_1(self) -> int:
        self._parse_input()
        Beam(
            direction=Beam.RIGHT,
            coordinates=(-1, 0),
            fields=self._fields,
            beams=self._beams,
        ).propagate()
        return ilen(x for x in self._beams.values() if x)

    @timeit
    @answer(7572)
    def part_2(self) -> int:
        self._parse_input()
        results = []
        for ln in range(self._max_size[0]):
            beams = deepcopy(self._beams)
            Beam(
                direction=Beam.RIGHT,
                coordinates=(-1, ln),
                fields=self._fields,
                beams=beams,
            ).propagate()
            results.append(ilen(x for x in beams.values() if x))
            beams = deepcopy(self._beams)
            Beam(
                direction=Beam.LEFT,
                coordinates=(self._max_size[1] + 1, ln),
                fields=self._fields,
                beams=beams,
            ).propagate()
            results.append(ilen(x for x in beams.values() if x))
        for ix in range(self._max_size[1]):
            beams = deepcopy(self._beams)
            Beam(
                direction=Beam.DOWN,
                coordinates=(ix, -1),
                fields=self._fields,
                beams=beams,
            ).propagate()
            results.append(ilen(x for x in beams.values() if x))
            beams = deepcopy(self._beams)
            Beam(
                direction=Beam.UP,
                coordinates=(ix, self._max_size[0] + 1),
                fields=self._fields,
                beams=beams,
            ).propagate()
            results.append(ilen(x for x in beams.values() if x))
        return max(results)

    def _parse_input(self):
        self._fields = {}
        self._beams: dict[tuple[int, int], list] = {}
        ln, ix = 0, 0
        for ln, line in enumerate(self.input):
            for ix, char in enumerate(line):
                self._fields[(ix, ln)] = char
                self._beams[(ix, ln)] = []
        self._max_size = (ln, ix)

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
