import math
from dataclasses import dataclass

try:
    from functools import cache
except ImportError:
    from functools import lru_cache as cache

from sneks.core.direction import Direction
from sneks.config.config import config


@dataclass(frozen=True)
class Cell:
    """
    Represents a single cell on the game board
    """

    row: int  #:
    column: int  #:

    @cache
    def __new__(cls, row: int, column: int) -> "Cell":
        return super().__new__(cls)

    def get_neighbor(self, direction: Direction) -> "Cell":
        """
        Gets a Cell's neighbor in the specified direction. Note that this does
        not perform any boundary checking and could return invalid cells

        :param direction: the direction of the neighbor
        :return: the neighbor cell in the specified direction
        """
        if direction is Direction.UP:
            return self.get_up()
        elif direction is Direction.DOWN:
            return self.get_down()
        elif direction is Direction.LEFT:
            return self.get_left()
        elif direction is Direction.RIGHT:
            return self.get_right()
        else:
            raise ValueError("direction not valid")

    def get_up(self) -> "Cell":
        """
        :return: cell in the up direction
        """
        return Cell(self.row - 1, self.column)

    def get_down(self) -> "Cell":
        """
        :return: cell in the down direction
        """
        return Cell(self.row + 1, self.column)

    def get_left(self) -> "Cell":
        """
        :return: cell in the left direction
        """
        return Cell(self.row, self.column - 1)

    def get_right(self) -> "Cell":
        """
        :return: cell in the right direction
        """
        return Cell(self.row, self.column + 1)

    def get_distance(self, other: "Cell") -> float:
        """
        Gets the distance between this cell and another

        :param other: cell to get distance to
        :return: distance between the two cells
        """
        return math.hypot(self.column - other.column, self.row - other.row)

    def is_valid(self) -> bool:
        """
        Checks if this cell is within the game board

        :return: True if the cell is in the board, False otherwise
        """
        return (
            0 <= self.row < config.game.rows and 0 <= self.column < config.game.columns
        )
