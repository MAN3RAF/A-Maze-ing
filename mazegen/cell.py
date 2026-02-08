class Cell:
    """
    Representation of a maze's cell.

    Attributes:
        neighbours (list[Cell]): The neighbours of the cell
        walls (dict[str, bool]): The walls of the cell in different directions
        visited (bool): Status in the backtracking algorithm
        reserved (bool): Is the cell in the 42 pattern at the mid
        x (int): x position of the cell
        y (int): y position of the cell
    """
    def __init__(self, x: int, y: int) -> None:
        """
        Initialise the cell, with it's (x, y) position in the maze.

        Args:
            x (int): X-coordinate of the cell
            y (int): Y-coordinate position of the cell
        """
        self.neighbours: list[Cell] = []
        self.walls: dict[str, bool] = {
            "south": True,
            "north": True,
            "east": True,
            "west": True
        }
        self.visited: bool = False
        self.reserved: bool = False
        self.path: bool = False
        self.x: int = x
        self.y: int = y

    def destroy_wall(self, direction: str) -> None:
        """
        Destroy the wall in the specified direction

        Args:
            direction (str): one of 'south', 'east', 'west', 'north'
        """
        self.walls[direction] = False

    def add_neighbour(self, cell: 'Cell') -> None:
        """
        Add the cell to the list of neighbours of self

        Args:
            cell (Cell): The cell to append to the neighbours
        """
        self.neighbours.append(cell)

    def count_wall(self) -> int:
        """Count how much closed wall does the cell have"""
        return len([v for v in self.walls.values() if v])

    def is_wall_between(self, n: 'Cell') -> bool:
        """
        Check if ther is a wall between the given neighbour n

        Args:
            n (Cell): Neighbour cell to check.

        Return:
            bool: True if wall between, False otherwise.
        """
        if n.x == self.x - 1:
            return self.walls['west']
        elif n.x == self.x + 1:
            return self.walls['east']
        elif n.y == self.y - 1:
            return self.walls['north']
        else:
            return self.walls['south']
