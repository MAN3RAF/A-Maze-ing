from mazegen.cell import Cell
from mazegen.solve import breadth_first_search
import random
from typing import Any
import time


class MazeGenerator:
    """
    Generate maze

    Args:
        width (int): Maze width
        height (int): Maze height
        start (list[int, int]): Maze entrance (for path)
        end (list[int, int]): = Maze exit (for path)
        seed (Optional[int]): Maze seed, if None generate random one
        algo (int): Generation algorithm to use
        self.displayer (Optional[Any]): Class to display the maze

    Methods:
        grid building:
            build_grid()
            set_neighbours()
            set_reserved()

        algorithms:
            backtracking()
            prims()
            kruskal()

        cell linking:
            link_two()
    """
    def __init__(self, width: int, height: int, start: tuple[int, int],
                 end: tuple[int, int], seed: int | None = None,
                 displayer: Any = None):
        """
        initialise the maze generator.

        Args:
            seed (Optional[int]): Maze seed, if None generate random one.
            algo (int): Generation algorithm to use, based on last seed digit.
                        0 = backtracking (defalt), 1 = prims, 2 = kruskal
            self.displayer (Optional[Any]): Class to display the maze.
            self.path (list[Cell]): Sequence of cells from entry to exit

        If you use your own displayer class and not the ShowMaze one,
        you need to change the following functions:
            user_option()
            link_two()
            backtracking()
            prims()
            kruskal()
        add the displaying function that you implemented.
        """
        self.width: int = width
        self.height: int = height
        self.start: tuple[int, int] = start
        self.end: tuple[int, int] = end

        self.seed: int = random.randint(1000, 5000)
        self.algo: int = 0
        if seed is not None and seed > 1:
            # The algorithm is the last seed digit, the seed take the rest
            self.seed = seed // 10
            self.algo = seed % 10

        self.displayer: Any = displayer
        self.path: list[Cell] = []
        self.path_visible: bool = False
        self.init_maze()

    def init_maze(self) -> None:
        """
        Initialise the grid, set the neighbours for each cells,
        set reserved cells for 42 pattern (is size allow it).

        Raises:
            ValueError: If entry or exit cell is reserved by the 42 pattern.
        """
        self.grid: list[list[Cell]] = self.build_grid()
        self.set_neighbours()
        self.set_reserved()

        # entry + exit verification
        if self.grid[self.start[1]][self.start[0]].reserved:
            raise ValueError("The entry is reserved by the 42 pattern, "
                             "change it's position pls")
        if self.grid[self.end[1]][self.end[0]].reserved:
            raise ValueError("The exit is reserved by the 42 pattern, "
                             "change it's position pls")

    def move_entry(self, x: int, y: int) -> None:
        """
        You can now move the entry like a player!

        Args:
            x (int): How much the cell moved horizontally
            y (int): How much the cell moved vertically
        """
        # Store the player based on coordinates
        player: Cell = self.grid[self.start[1]][self.start[0]]

        # Verify the x movement
        if ((x == 1 and not player.walls['east'])
                or (x == -1 and not player.walls['west'])):
            self.start = (self.start[0] + x, self.start[1])

        # Verify the y movement
        elif ((y == 1 and not player.walls['south'])
                or (y == -1 and not player.walls['north'])):
            self.start = (self.start[0], self.start[1] + y)

        # Update the grid when position changed
        if player.x != self.start[0] or player.y != self.start[1]:
            # if player moved in a path cell no need to redo BFS
            if self.grid[self.start[1]][self.start[0]].path:
                # Store the old path
                last_path = self.path
                self.path = self.path[1:]
            else:
                last_path = self.path
                # Apply bfs another time to refresh the shortest path
                self.path = breadth_first_search(self)

            # Set all cells in old path that are not in new path to False
            new_path = set(self.path)
            for cell in last_path:
                if cell not in new_path:
                    cell.path = False
                    self.displayer.update_cell(cell, self)

            # Set all cells in new path as the actual path visibility
            for cell in self.path:
                cell.path = self.path_visible

            # If path is visible refresh the display of it
            if self.path_visible:
                for cell in self.path:
                    self.displayer.update_cell(cell, self)

            # Update the past player cell and player cell
            self.displayer.update_cell(player, self)
            self.displayer.update_cell(self.grid[player.y + y][player.x + x],
                                       self)

    def switch_algo(self, direction: int) -> None:
        """
        Switch to the next or last algorithm

        direction (int): 1 or -1 to change the algo.
                        Use modulo 3 to get a result between 0 and 2.
        """
        self.algo = (self.algo + direction) % 3

    def user_option(self) -> None:
        """Display the user option using the displayer"""
        if self.displayer:
            self.displayer.user_option(self)

    def build_grid(self) -> list[list[Cell]]:
        """
        Build the grid and return it

        Returns:
            maze (list[list[Cell]]): 2d list of cells
        """
        maze: list[list[Cell]] = []
        for y in range(self.height):
            maze.append([])
            for x in range(self.width):
                maze[y].append(Cell(x, y))
        return maze

    def set_neighbours(self) -> None:
        """
        Set neighbours for each cell of the grid
        """
        for y, rows in enumerate(self.grid):
            for x, cell in enumerate(rows):
                if y < self.height - 1:
                    cell.add_neighbour(self.grid[y + 1][x])
                if y > 0:
                    cell.add_neighbour(self.grid[y - 1][x])
                if x < self.width - 1:
                    cell.add_neighbour(self.grid[y][x + 1])
                if x > 0:
                    cell.add_neighbour(self.grid[y][x - 1])

    def apply_algo(self, *args: Any, **kwargs: Any) -> None:
        """
        Apply a generation algorithm on the initialised grid,
        based on self.algo
        """
        self.init_maze()
        random.seed(self.seed)
        self.seed += 1
        if self.algo == 0:
            self.backtracking(*args, **kwargs)
        elif self.algo == 1:
            self.prims(*args, **kwargs)
        elif self.algo == 2:
            self.kruskal(*args, **kwargs)

    def set_reserved(self) -> None:
        """
        Set the cells reserved by the 42 pattern in the grid,
        if maze size allow it
        """
        if self.width < 9 or self.height < 7:
            return
        start_x = int(self.width / 2)
        start_y = int(self.height / 2)

        self.grid[start_y][start_x - 1].reserved = True
        self.grid[start_y][start_x - 2].reserved = True
        self.grid[start_y][start_x - 3].reserved = True

        self.grid[start_y][start_x + 1].reserved = True
        self.grid[start_y][start_x + 2].reserved = True
        self.grid[start_y][start_x + 3].reserved = True

        self.grid[start_y - 1][start_x + 3].reserved = True
        self.grid[start_y - 2][start_x + 3].reserved = True

        self.grid[start_y - 1][start_x - 3].reserved = True
        self.grid[start_y - 2][start_x - 3].reserved = True

        self.grid[start_y + 1][start_x - 1].reserved = True
        self.grid[start_y + 2][start_x - 1].reserved = True

        self.grid[start_y + 1][start_x + 1].reserved = True
        self.grid[start_y + 2][start_x + 1].reserved = True

        self.grid[start_y + 2][start_x + 2].reserved = True
        self.grid[start_y + 2][start_x + 3].reserved = True

        self.grid[start_y - 2][start_x + 1].reserved = True
        self.grid[start_y - 2][start_x + 2].reserved = True

    def save_maze(self, filename: str) -> None:
        """
        Save the maze's structure and the shortest path from entry to exit,
        into the output file.

        Args:
            filename (str): Path to the output file
        """
        with open(filename, 'w') as f:
            for rows in self.grid:
                for cell in rows:
                    # The maze structure is written in hexa format,
                    # each character tell us how much walls are closed
                    i = 0
                    if cell.walls['north']:
                        i += 1
                    if cell.walls['east']:
                        i += 2
                    if cell.walls['south']:
                        i += 4
                    if cell.walls['west']:
                        i += 8
                    f.write(f"{hex(i)[2:].capitalize()}")
                f.write('\n')
            f.write('\n')

            f.write(f"{self.start[0]},{self.start[1]}\n")
            f.write(f"{self.end[0]},{self.end[1]}\n")

            for i in range(1, len(self.path)):
                prev = self.path[i - 1]
                curr = self.path[i]

                # Write the direction taken from one cell to another
                if curr.x == prev.x + 1:
                    f.write("E")
                elif curr.x == prev.x - 1:
                    f.write("W")
                elif curr.y == prev.y + 1:
                    f.write("S")
                elif curr.y == prev.y - 1:
                    f.write("N")

    def save_seed(self) -> None:
        """
        Save the actual maze seed + algo used in seed.txt.

        Seed can be saved more than once in the file
        """
        with open("seed.txt", 'a') as f:
            f.write(f"{int((self.seed - 1) * 10 + self.algo)}\n")

    def unperfect(self, animate: bool) -> None:
        """
        Destroy some walls to make the maze unperfect

        Perfect maze: One path from entry to exit
        Unperfect maze: multiple path from entry to exit

        Args:
            animate (bool): Wether cells will be displayed one by one or not
        """
        candidates: list[tuple[Cell, Cell]] = []

        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                # Store destroyable cells, 3 walls + not reserved
                cell = self.grid[y][x]
                if not cell.reserved and cell.count_wall() == 3:
                    for n in cell.neighbours:
                        if not n.reserved and cell.is_wall_between(n):
                            candidates.append((cell, n))

        # Divide by 5 so we don't detroy too much
        random.shuffle(candidates)
        candidates = candidates[:int(len(candidates) / 5)]

        while candidates:
            # Remove a wall between the cell and a random neighbours
            actual, chosen = random.choice(candidates)
            self.link_two(actual, chosen, animate)
            candidates.remove((actual, chosen))

    def backtracking(self, perfect: bool, displaying: bool = False,
                     animate: bool = False) -> None:
        """
        Docstring for prims

        perfect (bool): True make the maze perfect, otherwise,
                        call self.unperfect() after maze generation.
        displaying (bool): True to display the maze.
        animate (bool): Whether the maze is displayed cell by cell.
        """
        my_stack = [self.grid[0][0]]

        while my_stack:
            # Pop the last cell and store it's available neighbours
            actual: Cell = my_stack.pop()
            available: list[Cell] = [n for n in actual.neighbours
                                     if not n.visited and not n.reserved]
            # Mark it as visited
            actual.visited = True
            if available:
                # Chose a random neighbour and link it with the cell
                chosen = random.choice(available)
                self.link_two(actual, chosen, animate)
                # Append the actual then chosen so it is the next popped
                my_stack.append(actual)
                my_stack.append(chosen)

        if not perfect:
            self.unperfect(animate)
        self.path = breadth_first_search(self)
        if self.displayer and displaying:
            self.displayer.display_grid(self)

    def prims(self, perfect: bool, displaying: bool = False,
              animate: bool = False) -> None:
        """
        Docstring for prims

        perfect (bool): True make the maze perfect, otherwise,
                        call self.unperfect() after maze generation.
        displaying (bool): True to display the maze.
        animate (bool): Whether the maze is displayed cell by cell.
        """
        start = self.grid[0][0]
        my_maze = [start]
        neighbours = []

        # Append tupple of cells that can be linked
        for cell in start.neighbours:
            if not cell.reserved:
                neighbours.append((start, cell))

        while neighbours:
            cell, next_cell = random.choice(neighbours)
            neighbours.remove((cell, next_cell))
            # Verify if we already linked this cell
            if next_cell in my_maze:
                continue
            # Append so we don't relink it
            my_maze.append(next_cell)
            self.link_two(cell, next_cell, animate)
            for cell in next_cell.neighbours:
                if cell not in my_maze and not cell.reserved:
                    # Append other tupples of possible linked cells
                    neighbours.append((next_cell, cell))

        if not perfect:
            self.unperfect(animate)
        self.path = breadth_first_search(self)
        if self.displayer and displaying:
            self.displayer.display_grid(self)

    def kruskal(self, perfect: bool, displaying: bool = False,
                animate: bool = False) -> None:
        """
        Docstring for prims

        perfect (bool): True make the maze perfect, otherwise,
                        call self.unperfect() after maze generation.
        displaying (bool): True to display the maze.
        animate (bool): Whether the maze is displayed cell by cell.
        """
        all_links = [{cell} for rows in self.grid
                     for cell in rows
                     if not cell.reserved]

        # While we didn't linked all cells into one set
        while len(all_links) != 1:
            my_set = random.choice(all_links)
            # Because sets are already random, we need a way to
            # derandomize it using sort
            actual = random.choice(list(
                sorted(
                    my_set,
                    key=lambda x: (len(x.neighbours), x.x, x.y)
                )
            )
            )
            # available cells
            unvisited = [cell for cell in actual.neighbours
                         if not cell.reserved]
            # do not compute if there is less than 2
            if len(unvisited) < 2:
                continue
            chosen = random.choice(unvisited)
            unvisited.remove(chosen)
            # Verify that chosen is not already in the same set
            # no loop protection + no link between same sets
            if chosen in my_set:
                continue
            for cell in all_links:
                # Search for the set that store chosen so we link thems
                if chosen in cell:
                    my_set.update(cell)
                    all_links.remove(cell)
                    self.link_two(actual, chosen, animate)
                    break

        if not perfect:
            self.unperfect(animate)
        self.path = breadth_first_search(self)
        if self.displayer and displaying:
            self.displayer.display_grid(self)

    def link_two(self, cell_1: Cell, cell_2: Cell, animate: bool) -> None:
        """
        Destroy the wall between cell_1 and cell_2.

        cell_1 and cell_2 need to be neighbours

        Args:
            cell_1 (Cell): Neighbour of cell_2
            cell_2 (Cell): Neighbour of cell_1   :)
            animate (bool): Whether cells will be displayed one by one or not
        """
        if cell_2.x == cell_1.x + 1:
            cell_2.destroy_wall('west')
            cell_1.destroy_wall('east')
        elif cell_2.x == cell_1.x - 1:
            cell_2.destroy_wall('east')
            cell_1.destroy_wall('west')
        elif cell_2.y == cell_1.y + 1:
            cell_2.destroy_wall('north')
            cell_1.destroy_wall('south')
        else:
            cell_2.destroy_wall('south')
            cell_1.destroy_wall('north')
        if animate and self.displayer:
            self.displayer.update_cell(cell_1, self)
            self.displayer.update_cell(cell_2, self)
            time.sleep(0.02)
