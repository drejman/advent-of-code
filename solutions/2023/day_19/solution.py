# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/19

from copy import deepcopy
from dataclasses import dataclass
from math import prod
from typing import NamedTuple

from ...base import StrSplitSolution, answer, timeit


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int


@dataclass
class Interval:
    min: int
    max: int

    def is_valid(self) -> bool:
        return self.min <= self.max

    def __len__(self) -> int:
        return self.max - self.min + 1


@dataclass
class PartsInterval:
    x: Interval
    m: Interval
    a: Interval
    s: Interval

    def combinations(self) -> int:
        return prod(len(attr) for attr in vars(self).values())


class Condition(NamedTuple):
    attribute: str
    sign: str
    value: int
    dest_workflow: str


class Workflow:
    def __init__(self, workflow_parts: list[str], final_dest_workflow: str) -> None:
        self.conditions: list[Condition] = []
        for workflow_part in workflow_parts:
            condition, result = workflow_part.split(":")
            self.conditions.append(
                Condition(condition[0], condition[1], int(condition[2:]), result)
            )
        self.final_dest_workflow = final_dest_workflow

    def work(self, part: Part) -> str:
        for condition in self.conditions:
            attr = getattr(part, condition.attribute)
            if condition.sign == ">" and attr > condition.value:
                return condition.dest_workflow
            if condition.sign == "<" and attr < condition.value:
                return condition.dest_workflow
        return self.final_dest_workflow

    def work_interval(self, part: PartsInterval) -> list[tuple[str, PartsInterval]]:
        parts = []
        for condition in self.conditions:
            accept_part = deepcopy(part)
            attr_interval: Interval = getattr(accept_part, condition.attribute)
            if condition.sign == ">":
                accept_interval = Interval(
                    min=condition.value + 1, max=attr_interval.max
                )
                reject_interval = Interval(min=attr_interval.min, max=condition.value)
            elif condition.sign == "<":
                accept_interval = Interval(
                    min=attr_interval.min, max=condition.value - 1
                )
                reject_interval = Interval(min=condition.value, max=attr_interval.max)
            else:
                raise ValueError
            if accept_interval.is_valid():
                setattr(accept_part, condition.attribute, accept_interval)
                parts.append((condition.dest_workflow, accept_part))
            if not reject_interval.is_valid():
                return parts
            setattr(part, condition.attribute, reject_interval)
        else:
            parts.append((self.final_dest_workflow, part))
        return parts


class Solution(StrSplitSolution):
    _year = 2023
    _day = 19
    first_workflow_name = "in"

    @timeit
    @answer(280909)
    def part_1(self) -> int:
        self._parse_input()
        self._accepted = []
        while self._parts:
            workflow_name, part = self._parts.pop()
            name = self._workflows[workflow_name].work(part)
            if name == "A":
                self._accepted.append(part)
            elif name == "R":
                continue
            else:
                self._parts.append((name, part))
        return sum(map(sum, self._accepted))

    @timeit
    @answer(116138474394508)
    def part_2(self) -> int:
        self._parse_input()
        initial_parts_interval = PartsInterval(*([Interval(min=1, max=4000)] * 4))
        self._parts_intervals = [(self.first_workflow_name, initial_parts_interval)]
        self._accepted_intervals = []

        while self._parts_intervals:
            workflow_name, input_parts_interval = self._parts_intervals.pop()
            result = self._workflows[workflow_name].work_interval(input_parts_interval)
            for name, output_parts_interval in result:
                if name == "A":
                    self._accepted_intervals.append(output_parts_interval)
                elif name == "R":
                    continue
                else:
                    self._parts_intervals.append((name, output_parts_interval))

        return sum(interval.combinations() for interval in self._accepted_intervals)

    def _parse_input(self):
        self._workflows = {}
        ln = 0
        for ln, line in enumerate(self.input):
            if line == "":
                break

            name, rest = line.split("{")
            rest = rest.removesuffix("}")
            workflow = rest.split(",")
            self._workflows[name] = Workflow(
                workflow_parts=workflow[:-1], final_dest_workflow=workflow[-1]
            )

        self._parts = []
        for line in self.input[ln + 1 :]:
            line = line.removeprefix("{").removesuffix("}")
            self._parts.append(
                (
                    self.first_workflow_name,
                    (
                        Part(
                            *(
                                int(x)
                                for atr in line.split(",")
                                for x in atr.split("=")
                                if x.isdigit()
                            )
                        )
                    ),
                )
            )
