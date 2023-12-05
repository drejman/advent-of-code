# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/5

import math
from copy import deepcopy
from functools import reduce
from typing import Self

from ...base import StrSplitSolution, answer


class LinearMapping:
    def __init__(
        self, source_starts: list[int], dest_starts: list[int], ranges: list[int]
    ):
        # reformat to: (start, stop=start+range, shift=destination-start)
        mapping = [
            (s, s + r, d - s) for s, d, r in zip(source_starts, dest_starts, ranges)
        ]
        self._sort_mapping(mapping)
        self._add_extreme_intervals(mapping)
        self._make_intervals_continuous(mapping)
        self._sort_mapping(mapping)
        self.mapping: tuple[tuple[int, int, int], ...] = tuple(mapping)

    def _add_extreme_intervals(self, mapping):
        mapping.append((mapping[-1][1], math.inf, 0))
        if mapping[0][0] != 0:
            mapping.append((0, mapping[0][0], 0))

    @staticmethod
    def _sort_mapping(mapping):
        mapping.sort(key=lambda x: x[0])

    @staticmethod
    def _make_intervals_continuous(mapping):
        records_to_add = []
        for index, (start, stop, shift) in enumerate(mapping[:-2]):
            if stop != mapping[index + 1][0]:
                records_to_add.append((stop, mapping[index + 1][0], 0))
        mapping.extend(records_to_add)

    def __repr__(self) -> str:
        repr = "Mapping Generator:"
        for map_ in self.mapping:
            repr += f"\n({map_[0]}-{map_[1]}) -> ({map_[0]+map_[2]}-{map_[1]+map_[2]})"
        return repr

    def get(self, source: int) -> int:
        for start, stop, shift in self.mapping:
            if start <= source < stop:
                return source + shift
        else:
            return source

    def get_index(self, source: int) -> int:
        for index, (start, stop, _) in enumerate(self.mapping):
            if start <= source < stop:
                return index
        else:
            return source

    def combine(self, other: Self) -> Self:
        new_mapping = []
        start = 0

        while True:
            self_index = self.get_index(start)
            other_index = other.get_index(self.get(start))
            end = min(
                self.mapping[self_index][1],
                max(other.mapping[other_index][1] - self.mapping[self_index][2], 0),
            )
            shift = self.mapping[self_index][2] + other.mapping[other_index][2]
            new_mapping.append((start, end, shift))
            if end == math.inf:
                break
            start = end

        self._make_intervals_continuous(new_mapping)
        self._sort_mapping(new_mapping)
        self.mapping = tuple(new_mapping)
        return self


class Solution(StrSplitSolution):
    _year = 2023
    _day = 5

    @answer(196167384)
    def part_1(self) -> int:
        self._parse_seeds_part_1()

        self._parse_input()
        locations = []
        for seed in self.seeds:
            current_value = seed
            for mappping in self.mappings:
                current_value = mappping.get(current_value)
            else:
                locations.append(current_value)
        return min(locations)

    @answer(125742456)
    def part_2(self) -> int:
        self._parse_seeds_part_2()
        self._parse_input()
        mappings = deepcopy(self.mappings)
        final_mapping = reduce(lambda x, y: x.combine(y), mappings)

        for start, stop, _ in sorted(final_mapping.mapping, key=lambda x: x[0] + x[2]):
            for seeds_start, seeds_stop in self.seed_ranges:
                if overlap := self._interval_overlap(
                    interval1=(start, stop), interval2=(seeds_start, seeds_stop)
                ):
                    return final_mapping.get(overlap[0])
        else:
            raise ValueError("Solution not found")

    @staticmethod
    def _interval_overlap(
        interval1: tuple[int, int], interval2: tuple[int, int]
    ) -> tuple[int, int] | None:
        begin = max(interval1[0], interval2[0])
        end = min(interval1[1], interval2[1])
        if begin > end:
            return None
        return (begin, end)

    def get_location(self, i):
        current_value = i
        for map_ in self.mappings:
            current_value = map_.get(current_value)
        else:
            return current_value

    def _parse_input(self):
        self.mappings: list[LinearMapping] = []
        current_list: list[tuple[int, int, int]] = []
        for line in self.input[2:]:
            match line:
                case map_start if "map" in map_start:
                    current_list = []
                case "":
                    dest_starts = [x[0] for x in current_list]
                    source_starts = [x[1] for x in current_list]
                    ranges = [x[2] for x in current_list]
                    self.mappings.append(
                        LinearMapping(
                            source_starts=source_starts,
                            dest_starts=dest_starts,
                            ranges=ranges,
                        )
                    )
                case line:
                    dest_start, source_start, range_len = list(
                        map(int, line.lstrip().strip().split(" "))
                    )
                    current_list.append((dest_start, source_start, range_len))
        else:
            dest_starts = [x[0] for x in current_list]
            source_starts = [x[1] for x in current_list]
            ranges = [x[2] for x in current_list]
            self.mappings.append(
                LinearMapping(
                    source_starts=source_starts, dest_starts=dest_starts, ranges=ranges
                )
            )

    def _parse_seeds_part_1(self):
        self.seeds: list[int] = []
        _, numbers = self.input[0].split(":")
        numbers = list(map(int, numbers.lstrip().strip().split(" ")))
        self.seeds = numbers

    def _parse_seeds_part_2(self):
        self.seed_ranges: list[tuple[int, int]] = []
        _, numbers = self.input[0].split(":")
        numbers = list(map(int, numbers.lstrip().strip().split(" ")))
        for i in range(len(numbers) // 2):
            self.seed_ranges.append(
                (numbers[2 * i], numbers[2 * i] + numbers[2 * i + 1])
            )
        self.seed_ranges.sort(key=lambda x: x[0])
