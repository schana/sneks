import abc
from typing import List, Sequence, FrozenSet

from sneks.core.cell import Cell
from sneks.core.direction import Direction


class Snek(abc.ABC):
    """
    Base snek from which submission sneks derive. This snek has no behavior.
    """

    #: Body of the snek represented as a list of cells, with index 0 being the head
    body: List[Cell] = []
    #: Set of currently occupied cells on the game board
    occupied: FrozenSet[Cell] = []
    #: Set of cells that contain food on the game board
    food: FrozenSet[Cell] = []

    def get_next_direction(self) -> Direction:
        """
        Method that determines which way the snek should go next

        :return: the next direction for the snek to move
        """
        raise NotImplementedError()

    def get_head(self) -> Cell:
        """
        Helper method to return the first cell from the snek's body

        :return: the cell representing the head of the snake
        """
        return self.body[0]

    def get_body(self) -> List[Cell]:
        """
        Helper method to return the snek's body

        :return: the list of cells making up the snake, including the head
        """
        return self.body

    def get_food(self) -> FrozenSet[Cell]:
        """
        Helper method to return the current food on the board

        :return: the set of food on the game board
        """
        return self.food

    def get_closest_food(self) -> Cell:
        """
        Get the closest food to the head of the snek from the current set

        :return: the Cell representing the location of the nearest food
        """
        return min(self.food, key=lambda food: food.get_distance(self.get_head()))

    def look(self, direction: Direction) -> int:
        """
        Look in a direction from the snek's head and get the distance to the closest obstacle

        :param direction: the direction to look
        :return: the distance until the closest obstacle in the specified direction
        """

        current = self.get_head().get_neighbor(direction)
        current_distance = 1

        while current not in self.occupied and current.is_valid():
            current = current.get_neighbor(direction)
            current_distance += 1

        return current_distance - 1

    def get_direction_to_destination(
        self,
        destination: Cell,
        directions: Sequence[Direction] = (
            Direction.UP,
            Direction.DOWN,
            Direction.LEFT,
            Direction.RIGHT,
        ),
    ) -> Direction:
        """
        Get the next direction to travel in order to reach the destination
        from a set of specified directions (default: all directions)

        When multiple directions have the same resulting distance, the chosen
        direction is determined by the order provided, with directions coming
        first having precedence

        :param destination: the cell to travel towards
        :param directions: the directions to evaluate in order
        :return: the direction to travel that will close the most distance
        """

        return min(
            directions,
            key=lambda direction: self.get_head()
            .get_neighbor(direction)
            .get_distance(destination),
        )
