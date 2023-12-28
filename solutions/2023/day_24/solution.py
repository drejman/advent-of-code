# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/24

from dataclasses import dataclass
from itertools import combinations
from statistics import median
from typing import Self

import numpy as np
from shapely import intersection
from shapely.geometry import LineString, Point

from ...base import StrSplitSolution, answer, timeit


@dataclass
class MovingPoint3D:
    px: int
    py: int
    pz: int
    vx: int
    vy: int
    vz: int
    min_value: int
    max_value: int
    _line_segment: LineString | None = None
    _max_time: float = 0.0
    _min_time: float = 0.0

    @property
    def max_time(self) -> float:
        if self._max_time != 0.0:
            return self._max_time
        self._calculate_time()
        return self._max_time

    def _calculate_time(self):
        x_t_min, x_t_max = sorted(
            [(self.min_value - self.px) / self.vx, (self.max_value - self.px) / self.vx]
        )
        y_t_min, y_t_max = sorted(
            [(self.min_value - self.py) / self.vy, (self.max_value - self.py) / self.vy]
        )
        self._max_time = min(x_t_max, y_t_max)
        self._min_time = max(x_t_min, y_t_min, 0)

    @property
    def min_time(self) -> float:
        if self._min_time != 0.0:
            return self._min_time
        else:
            self._calculate_time()
            return self._min_time

    @property
    def line_segment(self) -> LineString:
        if self._line_segment:
            return self._line_segment
        self._line_segment = LineString(
            [
                (self.px, self.py),
                (self.px + self.vx * self.max_time, self.py + self.vy * self.max_time),
            ]
        )
        return self._line_segment

    def intersects(self, other: Self) -> bool:
        return self.line_segment.intersects(other.line_segment)


class Solution(StrSplitSolution):
    _year = 2023
    _day = 24

    @timeit
    @answer(20336)
    def part_1(self) -> int:
        self._parse_input()
        result = 0
        for point1, point2 in combinations(self._points, 2):
            test = intersection(point1.line_segment, point2.line_segment)
            if not isinstance(test, Point):
                continue
            if (
                self._time_beginning <= test.x <= self._time_end
                and self._time_beginning <= test.y <= self._time_end
            ):
                result += 1
        return result

    @timeit
    @answer(677656046662770)
    def part_2(self) -> int:
        solves = []
        for p1, p2, p3 in combinations(self._points, 3):
            px = [p1.px, p2.px, p3.px]
            py = [p1.py, p2.py, p3.py]
            pz = [p1.pz, p2.pz, p3.pz]
            vx = [p1.vx, p2.vx, p3.vx]
            vy = [p1.vy, p2.vy, p3.vy]
            vz = [p1.vz, p2.vz, p3.vz]
            A = np.array(
                [
                    [vy[1] - vy[0], vx[0] - vx[1], 0, py[0] - py[1], px[1] - px[0], 0],
                    [vy[2] - vy[0], vx[0] - vx[2], 0, py[0] - py[2], px[2] - px[0], 0],
                    [vz[1] - vz[0], 0, vx[0] - vx[1], pz[0] - pz[1], 0, px[1] - px[0]],
                    [vz[2] - vz[0], 0, vx[0] - vx[2], pz[0] - pz[2], 0, px[2] - px[0]],
                    [0, vz[1] - vz[0], vy[0] - vy[1], 0, pz[0] - pz[1], py[1] - py[0]],
                    [0, vz[2] - vz[0], vy[0] - vy[2], 0, pz[0] - pz[2], py[2] - py[0]],
                ]
            )

            x = [
                (py[0] * vx[0] - py[1] * vx[1]) - (px[0] * vy[0] - px[1] * vy[1]),
                (py[0] * vx[0] - py[2] * vx[2]) - (px[0] * vy[0] - px[2] * vy[2]),
                (pz[0] * vx[0] - pz[1] * vx[1]) - (px[0] * vz[0] - px[1] * vz[1]),
                (pz[0] * vx[0] - pz[2] * vx[2]) - (px[0] * vz[0] - px[2] * vz[2]),
                (pz[0] * vy[0] - pz[1] * vy[1]) - (py[0] * vz[0] - py[1] * vz[1]),
                (pz[0] * vy[0] - pz[2] * vy[2]) - (py[0] * vz[0] - py[2] * vz[2]),
            ]
            sol = np.linalg.solve(A, x)
            solves.append(sol[0] + sol[1] + sol[2])
        return round(median(solves))

    def _parse_input(self):
        self._time_beginning = 200000000000000
        self._time_end = 400000000000000
        if self.use_test_data:
            self._time_beginning = 7
            self._time_end = 27
        self._points = []
        for line in self.input:
            positions, velocities = line.split(" @ ")
            positions = map(int, positions.split(","))
            velocities = map(int, velocities.split(","))
            self._points.append(
                MovingPoint3D(
                    *positions,
                    *velocities,
                    min_value=self._time_beginning,
                    max_value=self._time_end,
                )
            )
