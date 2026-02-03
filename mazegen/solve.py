from mazegen.cell import Cell
from collections import deque
from typing import Any
import time


def get_accessible_neighbors(cell: Cell) -> list[Cell]:
    """Return neighbors that can be reached (no wall between)."""
    accessible = []
    for neighbor in cell.neighbours:
    #check if there is wall between the cell and its neighbor.
        if neighbor.x == cell.x + 1 and not cell.walls['east']:
            accessible.append(neighbor)
        elif neighbor.x == cell.x - 1 and not cell.walls['west']:
            accessible.append(neighbor)
        elif neighbor.y == cell.y + 1 and not cell.walls['south']:
            accessible.append(neighbor)
        elif neighbor.y == cell.y - 1 and not cell.walls['north']:
            accessible.append(neighbor)

    return accessible


def breadth_first_search(maze: Any) -> list[Cell] | None:
    """BFS to find shortest path from start to end in the maze."""
    
    start_x, start_y = maze.start
    end_x, end_y = maze.end
    
    start_cell = maze.grid[start_y][start_x]
    end_cell = maze.grid[end_y][end_x]
    
    relation = {cell: None for row in maze.grid for cell in row}
    all_paths = deque([start_cell])
    while all_paths:

        actual = all_paths.popleft()

        if actual == end_cell:
            break

        accessible = get_accessible_neighbors(actual)
        for neighbour in accessible:
            if not relation[neighbour] and neighbour != start_cell:
                relation[neighbour] = actual
                all_paths.append(neighbour)

    actual = end_cell
    path = deque([])
    while actual:
        path.appendleft(actual)
        actual = relation[actual]
    return path


def switch_path(path: list[Cell], displayer: Any = None, animate: bool = False, visible: bool | None = None) -> None:
    """Mark the path cells as reserved to highlight them in display."""
    for cell in path:
        if visible == None:
            if cell.path:
                cell.path = False
            else:
                cell.path = True
        else:
            cell.path = visible
        if animate and displayer:
            displayer.update_cell_v1(cell)
            time.sleep(0.01)
