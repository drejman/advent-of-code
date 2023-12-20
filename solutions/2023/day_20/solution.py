# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/20
from abc import ABC, abstractmethod
from collections import deque
from itertools import chain
from math import lcm

from ...base import StrSplitSolution, answer, timeit


class ResultReady(Exception):
    ...


class Module(ABC):
    @abstractmethod
    def work(self, input_pulse: int, **kwargs) -> int:
        pass


class FlipFlop(Module):
    def __init__(self):
        self._state = 0

    def work(self, input_pulse: int, **kwargs) -> int | None:
        if input_pulse == 1:
            return None
        new_ = int(not bool(self._state))
        self._state = new_
        return new_


class Conjunction(Module):
    def __init__(self, inputs: list[str]) -> None:
        self._inputs = {input_name: 0 for input_name in inputs}

    def work(self, input_pulse: int, input_name: str, **kwargs) -> int:
        self._inputs[input_name] = input_pulse
        if all(bool(v) for v in self._inputs.values()):
            return 0
        return 1


class SpecialConjunction(Conjunction):
    def __init__(self, inputs: list[str]) -> None:
        super().__init__(inputs)
        self._cycles = {input_name: [] for input_name in inputs}

    def work(self, input_pulse: int, input_name: str, cycle: int) -> int:
        if input_pulse == 1:
            self._cycles[input_name].append(cycle)
        if all(self._cycles.values()):
            raise ResultReady(lcm(*chain.from_iterable(self._cycles.values())))
        return super().work(input_pulse, input_name)


class Broadcaster(Module):
    def __init__(self) -> None:
        pass

    def work(self, input_pulse: int, **kwargs) -> int:
        return input_pulse


class Solution(StrSplitSolution):
    _year = 2023
    _day = 20
    end_node = None

    @timeit
    @answer(666795063)
    def part_1(self) -> int:
        self._parse_input()
        self._setup_modules()
        return self.warm_up_cables(iterations=1000)
    
    @timeit
    @answer(253302889093151)
    def part_2(self) -> int:
        self.end_node = "rx"
        self._parse_input()
        self._setup_modules()
        try:
            self.warm_up_cables(iterations=10000000, count_pulses=False)
        except ResultReady as result:
            return result.args[0]
        else:
            raise ValueError

    def warm_up_cables(self, iterations: int, count_pulses=True):
        def consume(q: deque):
            name, pulse, input_name = q.popleft()
            return name, pulse, input_name

        def consume_with_count(q: deque):
            name, pulse, input_name = consume(q)
            self._pulses_counter[pulse] += 1
            return name, pulse, input_name

        chosen_consume = consume
        if count_pulses:
            self._pulses_counter = {0: 0, 1: 0}
            chosen_consume = consume_with_count
        q = deque()
        i = 0
        for i in range(1, iterations + 1):
            q.append(("broadcaster", 0, "button"))
            new_pulse = None
            while q:
                name, pulse, input_name = chosen_consume(q=q)
                if module := self._modules.get(name):
                    new_pulse = module.work(
                        input_pulse=pulse, input_name=input_name, cycle=i
                    )
                if module is None or new_pulse is None:
                    continue
                for module in self._module_connections[name]:
                    q.append((module, new_pulse, name))
        return self._pulses_counter[0] * self._pulses_counter[1] if count_pulses else i

    def _parse_input(self):
        self._module_connections = {}
        self._module_types = {}
        for line in self.input:
            name, connections = line.split(" -> ")
            if name.startswith("%"):
                name = name.removeprefix("%")
                self._module_types[name] = "FlipFlop"
            elif name.startswith("&"):
                name = name.removeprefix("&")
                self._module_types[name] = "Conjunction"
            else:
                self._module_types[name] = "Broadcaster"
            self._module_connections[name] = connections.split(", ")

    def _setup_modules(self):
        self._modules: dict[str, Module] = {}
        for k, v in self._module_types.items():
            if v == "FlipFlop":
                module = FlipFlop()
            elif v == "Conjunction":
                inputs = list(
                    key for key, value in self._module_connections.items() if k in value
                )
                if self.end_node in self._module_connections[k]:
                    module = SpecialConjunction(inputs=inputs)
                else:
                    module = Conjunction(inputs=inputs)
            elif v == "Broadcaster":
                module = Broadcaster()
            else:
                raise ValueError
            self._modules[k] = module
