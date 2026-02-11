from mazegen.cell import Cell
from collections import deque
from typing import Any
import time


def get_accessible_neighbors(cell: Cell) -> list[Cell]:
    """
    Return neighbors that can be reached (no wall between).

    Args:
        cell (Cell): The cell to verify

    Return:
        accessible (list[Cell]): List of accessible neighbours
    """
    accessible = []
    for neighbor in cell.neighbours:
        if neighbor.x == cell.x + 1 and not cell.walls['east']:
            accessible.append(neighbor)
        elif neighbor.x == cell.x - 1 and not cell.walls['west']:
            accessible.append(neighbor)
        elif neighbor.y == cell.y + 1 and not cell.walls['south']:
            accessible.append(neighbor)
        elif neighbor.y == cell.y - 1 and not cell.walls['north']:
            accessible.append(neighbor)

    return accessible


def breadth_first_search(maze: Any) -> list[Cell]:
    """
    BFS (breadth first search) to find shortest path from
    start to end in the maze.

    Args:
        maze (MazeGenerator): The maze to generate the path from

    Return:
        list(path) (list): A list of cell representing the shortest
        path from the entry to the exit
    """
    start_x, start_y = maze.start
    end_x, end_y = maze.end

    # Initialise the start and end cell of the path
    start_cell = maze.grid[start_y][start_x]
    end_cell = maze.grid[end_y][end_x]

    # Initialise the relations between cells in a dict
    # [key=child: value=parent]
    relation: dict[Cell, Cell | None] = {cell: None
                                         for row in maze.grid
                                         for cell in row}
    # Store all cells that we will evaluate
    all_paths = deque([start_cell])
    while all_paths:

        # pop the leftest cell
        actual = all_paths.popleft()

        # stop the loop if we found the destination
        if actual == end_cell:
            break

        # get the accessible neighbours and iterate over it
        accessible = get_accessible_neighbors(actual)
        for neighbour in accessible:
            # Update the dict if the neighbours still do not have a
            # parent, if it have then there is a closes parent,
            # then append it to all_paths
            if not relation[neighbour] and neighbour != start_cell:
                relation[neighbour] = actual
                all_paths.append(neighbour)

    actual = end_cell
    path: deque[Cell] = deque([])
    # Append the parent to the path,
    # until we find Null (parent of the entrance)
    while actual:
        path.appendleft(actual)
        actual = relation[actual]
    return list(path)


def switch_path(path: list[Cell], maze: Any,
                animate: bool = False,
                visible: bool | None = None) -> None:
    """
    Toggle the visibility of the path in the maze

    Visibility can be determined by:
        1) The 'visible' parameter given (option)
        2) Otherwise, Cell are toggled True->False or False->True

    if animate is set to True, animate the path cell by cell

    Args:
        path (list[Cell]): The path to show or hide
        displayer (Optional[ShowMaze]): The class to display cells
        animate (Optional[bool]): Displaying the cell one by one
        visible (Optional[bool]): Path visibility, True to show False to hide
    """
    for cell in path:
        if visible is None:
            if cell.path:
                cell.path = False
            else:
                cell.path = True
        else:
            cell.path = visible
    if animate and maze.displayer:
        for cell in path:
            maze.displayer.update_cell(cell, maze)
            time.sleep(0.01)
        maze.displayer.update_cell(maze.grid[maze.end[1]]
                                   [maze.end[0]], maze)
        maze.displayer.update_cell(maze.grid[maze.start[1]]
                                   [maze.start[0]], maze)
