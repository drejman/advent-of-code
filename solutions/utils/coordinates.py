from typing import NamedTuple, Self


class Coordinates(NamedTuple):
    col: int
    row: int

    def __add__(self, other: Self) -> Self:
        return type(self)(col=self.col + other.col, row=self.row + other.row)
