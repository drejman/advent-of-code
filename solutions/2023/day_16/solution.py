# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/16

import queue
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from functools import cache
from uuid import uuid4

from more_itertools import ilen

from ...base import StrSplitSolution, answer, timeit


@dataclass(eq=True, frozen=True)
class BeamData:
    direction: str
    coordinates: tuple[int, int]


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
    ):
        self.id = uuid4()
        self.direction = direction
        self.coordinates = coordinates
        self.fields = fields

    def propagate(self) -> tuple[set[tuple[int, int]], list[BeamData]]:
        visited = []
        splitted = []
        while True:
            next_coordinates = self._calculate_next_field()
            if not (next_field := self.fields.get(next_coordinates)):
                break

            self.coordinates = next_coordinates
            visited.append(self.coordinates)

            match next_field, self.direction:
                case "|", (self.LEFT | self.RIGHT):
                    splitted = [
                        BeamData(
                            direction=self.UP,
                            coordinates=next_coordinates,
                        ),
                        BeamData(
                            direction=self.DOWN,
                            coordinates=next_coordinates,
                        ),
                    ]
                    break
                case "-", (self.UP | self.DOWN):
                    splitted = [
                        BeamData(
                            direction=self.LEFT,
                            coordinates=next_coordinates,
                        ),
                        BeamData(
                            direction=self.RIGHT,
                            coordinates=next_coordinates,
                        ),
                    ]
                    break
                case "\\", self.LEFT:
                    self.direction = self.UP
                case "\\", self.DOWN:
                    self.direction = self.RIGHT
                case "\\", self.RIGHT:
                    self.direction = self.DOWN
                case "\\", self.UP:
                    self.direction = self.LEFT
                case "/", self.LEFT:
                    self.direction = self.DOWN
                case "/", self.DOWN:
                    self.direction = self.LEFT
                case "/", self.RIGHT:
                    self.direction = self.UP
                case "/", self.UP:
                    self.direction = self.RIGHT
                case _, _:
                    pass
        return set(visited), splitted

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
        return self.get_energized_count(
            beam_data=BeamData(
                direction=Beam.RIGHT,
                coordinates=(-1, 0),
            ),
            energized=deepcopy(self._beams),
        )

    @timeit
    @answer(7572)
    def part_2(self) -> int:
        self._parse_input()
        results = []

        for ln in range(self._max_size[0]):
            results.append(
                self.get_energized_count(
                    beam_data=BeamData(
                        direction=Beam.RIGHT,
                        coordinates=(-1, ln),
                    ),
                    energized=deepcopy(self._beams),
                )
            )

            results.append(
                self.get_energized_count(
                    beam_data=BeamData(
                        direction=Beam.LEFT,
                        coordinates=(self._max_size[1] + 1, ln),
                    ),
                    energized=deepcopy(self._beams),
                )
            )

        for ix in range(self._max_size[1]):
            results.append(
                self.get_energized_count(
                    beam_data=BeamData(
                        direction=Beam.DOWN,
                        coordinates=(ix, -1),
                    ),
                    energized=deepcopy(self._beams),
                )
            )

            results.append(
                self.get_energized_count(
                    beam_data=BeamData(
                        direction=Beam.UP,
                        coordinates=(ix, self._max_size[0] + 1),
                    ),
                    energized=deepcopy(self._beams),
                )
            )

        return max(results)

    @cache
    def propagate(self, beam_data: BeamData):
        return Beam(
            direction=beam_data.direction,
            coordinates=beam_data.coordinates,
            fields=self._fields,
        ).propagate()

    def get_energized_count(
        self, beam_data: BeamData, energized: dict[tuple[int, int], int]
    ) -> int:
        beams = queue.Queue()
        seen = set()
        beams.put(beam_data)
        while not beams.empty():
            beam = beams.get_nowait()
            visited, splitted = self.propagate(beam_data=beam)
            for beam in splitted:
                if (beam.direction, beam.coordinates) not in seen:
                    beams.put_nowait(beam)
                    seen.add((beam.direction, beam.coordinates))
            for coords in visited:
                energized[coords] += 1
        return ilen(x for x in energized.values() if x)

    def _parse_input(self):
        self._fields = {}
        self._beams: dict[tuple[int, int], int] = defaultdict(int)
        ln, ix = 0, 0
        for ln, line in enumerate(self.input):
            for ix, char in enumerate(line):
                self._fields[(ix, ln)] = char
        self._max_size = (ln, ix)
