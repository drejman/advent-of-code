# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2023/day/10

from ...base import StrSplitSolution, answer, timeit


class Solution(StrSplitSolution):
    _year = 2023
    _day = 10

    @timeit
    @answer(7173)
    def part_1(self) -> int:
        coordinates = self._initialize_graph()
        return self._analyze_neighborhood(coordinates=coordinates)

    @timeit
    @answer(291)
    def part_2(self) -> int:
        coordinates = self._initialize_graph()
        self._analyze_neighborhood(coordinates=coordinates)
        self.char_mapping = {
            "|": chr(int("0x2502", 0)),
            "-": chr(int("0x2500", 0)),
            "7": chr(int("0x2510", 0)),
            "L": chr(int("0x2514", 0)),
            "F": chr(int("0x250C", 0)),
            "J": chr(int("0x2518", 0)),
            }
        self.char_mapping["S"]=self.char_mapping["7"]
        input_ = ""
        count = 0
        for h, line in enumerate(self.input):
            in_ = False
            for w, _ in enumerate(line):
                if self.graph.get((w,h)):
                    if self.input[h][w] in "|7FS":
                        in_ = not in_
                    input_ += self.char_mapping[self.input[h][w]]
                else:
                    if in_:
                        count += 1
                        input_ += chr(9632)
                    else:
                        input_ += chr(9633)
            input_ += "\n"
        self.debug(input_)
        return count


    def _initialize_graph(self):
        self.height = len(self.input)
        self.width = len(self.input[0])
        self.graph: dict[tuple[int, int], list] = {}
        coordinates: tuple[int, int] = (-1, -1)
        for h, line in enumerate(self.input):
            if (w := line.find("S")) != -1:
                coordinates = (w, h)
                self.graph[coordinates] = []
        self.debug(self.graph)
        return coordinates

    def _analyze_neighborhood(self, coordinates: tuple[int, int]):
        self.debug(coordinates)
        w, h = coordinates
        neighborhood = []
        for shift_w, shift_h in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            if 0 <= w + shift_w < self.width and 0 <= h + shift_h < self.height:
                neighborhood.append((shift_w, shift_h))
        # self.debug(neighborhood)
        result = []
        for initial_shift_w, initial_shift_h in neighborhood:
            w, h = coordinates
            shift_w, shift_h = initial_shift_w, initial_shift_h  # 0, 1
            char = self.input[h+shift_h][w+shift_w]  # | [3][0]
            self.debug(f"{char} [{h+shift_h}] [{w+shift_w}]")
            counter = 0
            while char != "S":
                match char, shift_w, shift_h:
                    case [".", _, _]:
                        break
                    case ["|", 0, -1 | 1]:
                        # add coordinate to the graph because match
                        self.graph[(w, h)].append((w+shift_w, h+shift_h))  # [0,2] = [(0,3), ]

                        # new coordinates
                        w += shift_w  # 0
                        h += shift_h  # 3
                        self.graph[(w, h)] = []  # [0,3] = []

                        # next step to analyze based on shape and direction of travel
                        shift_h = shift_h  # 1
                        shift_w = shift_w  # 0
                    case ["-", -1 | 1, 0]:
                        # add coordinate to the graph because match
                        self.graph[(w, h)].append((w+shift_w, h+shift_h))  # [1,3] = [(2,3), ]

                        # new coordinates
                        w += shift_w  # 2
                        h += shift_h  # 3
                        self.graph[(w, h)] = []  # [2,3] = []
                        
                        # next step to analyze based on shape and direction of travel
                        shift_h = shift_h  # 0
                        shift_w = shift_w  # 1
                    case ["L", -1, 0]:
                        # add coordinate to the graph because match
                        self.graph[(w, h)].append((w+shift_w, h+shift_h))

                        # new coordinates
                        w += shift_w
                        h += shift_h
                        self.graph[(w, h)] = []
                        
                        # next step to analyze based on shape and direction of travel
                        shift_h = -1
                        shift_w = 0
                    case ["L", 0, 1]:
                        # add coordinate to the graph because match
                        self.graph[(w, h)].append((w+shift_w, h+shift_h)) # [0,3] = [(0,4), ]

                        # new coordinates
                        w += shift_w  # 0
                        h += shift_h  # 4
                        self.graph[(w, h)] = []  # [0,4] = []
                        
                        # next step to analyze based on shape and direction of travel
                        shift_h = 0 
                        shift_w = 1
                    case ["J", 1, 0]:
                        # add coordinate to the graph because match
                        self.graph[(w, h)].append((w+shift_w, h+shift_h)) # [0,4] = [(1,4), ]

                        # new coordinates
                        w += shift_w  # 1
                        h += shift_h  # 4
                        self.graph[(w, h)] = []  # [1,4] = []
                        
                        # next step to analyze based on shape and direction of travel
                        shift_h = -1 
                        shift_w = 0
                    case ["J", 0, 1]:
                        # add coordinate to the graph because match
                        self.graph[(w, h)].append((w+shift_w, h+shift_h))

                        # new coordinates
                        w += shift_w
                        h += shift_h
                        self.graph[(w, h)] = []
                        
                        # next step to analyze based on shape and direction of travel
                        shift_h = 0 
                        shift_w = -1
                    case ["F", 0, -1]:
                        # add coordinate to the graph because match
                        self.graph[(w, h)].append((w+shift_w, h+shift_h))

                        # new coordinates
                        w += shift_w
                        h += shift_h
                        self.graph[(w, h)] = []
                        
                        # next step to analyze based on shape and direction of travel
                        shift_h = 0
                        shift_w = 1
                    case ["F", -1, 0]:
                        # add coordinate to the graph because match
                        self.graph[(w, h)].append((w+shift_w, h+shift_h))

                        # new coordinates
                        w += shift_w
                        h += shift_h
                        self.graph[(w, h)] = []
                        
                        # next step to analyze based on shape and direction of travel
                        shift_h = 1
                        shift_w = 0
                    case ["7", 1, 0]:
                        # add coordinate to the graph because match
                        self.graph[(w, h)].append((w+shift_w, h+shift_h))

                        # new coordinates
                        w += shift_w
                        h += shift_h
                        self.graph[(w, h)] = []
                        
                        # next step to analyze based on shape and direction of travel
                        shift_h = 1
                        shift_w = 0
                    case ["7", 0, -1]:
                        # add coordinate to the graph because match
                        self.graph[(w, h)].append((w+shift_w, h+shift_h))

                        # new coordinates
                        w += shift_w
                        h += shift_h
                        self.graph[(w, h)] = []
                        
                        # next step to analyze based on shape and direction of travel
                        shift_h = 0
                        shift_w = -1
                    case _:
                        break
                try:
                    char = self.input[h+shift_h][w+shift_w] # 1: L [4][0]; 2: J [4][1]; 3: F [3][1]; 4: [3][2]
                    counter += 1
                    # self.debug(char)
                except IndexError:
                    break
            else:
                self.graph[(w, h)].append((w+shift_w, h+shift_h))
            result.append(counter)
        self.debug(result)
        return (min([r for r in result if r != 0]) + 1) // 2
