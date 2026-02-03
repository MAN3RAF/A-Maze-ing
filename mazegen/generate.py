from mazegen.cell import Cell
import random
from typing import Any
import time
import curses


class MazeGenerator:
    def __init__(self, width: int, height: int, start: tuple[int, int],
                 end: tuple[int, int], seed: int | None=None,
                 displayer: Any = None):
        self.width = width
        self.height = height
        self.start = start
        self.end = end
        self.seed = seed
        self.displayer = displayer
        self.init_maze()
        

    def init_maze(self) -> None:
        self.grid: list[list[Cell]] = self.build_grid()
        self.set_neighbours()
        self.set_reserved()

        if self.grid[self.start[1]][self.start[0]].reserved:
            raise ValueError("The entry is reserved by the 42 pattern, change it's "
                             "position pls")
        if self.grid[self.end[1]][self.end[0]].reserved:
            raise ValueError("The exit is reserved by the 42 pattern, change it's "
                             "position pls")

    def build_grid(self) -> list[list[Cell]]:
        maze: list = []
        for y in range(self.height):
            maze.append([])
            for x in range(self.width):
                maze[y].append(Cell(x, y))
        return maze

    def set_neighbours(self) -> None:
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

    def set_reserved(self) -> None:
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

    def save_maze(self, filename, path):    # save the output file
        with open(filename, 'w') as f:
            for rows in self.grid:
                for cell in rows:
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

            for i in range(1, len(path)):
                prev = path[i - 1]
                curr = path[i]

                if curr.x == prev.x + 1:
                    f.write("E")
                elif curr.x == prev.x - 1:
                    f.write("W")
                elif curr.y == prev.y + 1:
                    f.write("S")
                elif curr.y == prev.y - 1:
                    f.write("N")

    def save_seed(self): #save seed
        with open("seed.txt", 'w') as f:
            f.write(f"\n{self.seed}")

    def unperfect(self, animate: bool):
        candidates = []

        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                cell = self.grid[y][x]
                if not cell.reserved and cell.count_wall() == 3:
                    for n in cell.neighbours:
                        if not n.reserved and cell.is_wall_between(n):
                            candidates.append((cell, n))

        random.shuffle(candidates)
        candidates = candidates[:int(len(candidates) / 4)]
        while candidates:
            actual, chosen = random.choice(candidates)
            self.link_two(actual, chosen, animate)
            candidates.remove((actual, chosen))

    def backtracking(self, perfect, animate: bool=False) -> int:
        curses.curs_set(0)
        if self.seed == None:
            self.seed = random.randint(1000, 5000)
        random.seed(self.seed)
        my_stack = [self.grid[0][0]]

        while my_stack:
            actual: Cell = my_stack.pop()
            unvisited: list[Cell] = [n for n in actual.neighbours if not n.visited and not n.reserved]
            actual.visited = True
            if unvisited:
                chosen = random.choice(unvisited)
                self.link_two(actual, chosen, animate)
                my_stack.append(actual)
                my_stack.append(chosen)

        if not perfect:
            self.unperfect(animate)
        if self.displayer:
            self.displayer.display_grid()

    def prims(self, perfect: bool, animate: bool=False) -> int:
        curses.curs_set(0)
        if self.seed == None:
            self.seed = random.randint(1000, 5000)
        random.seed(self.seed)
        start = self.grid[0][0]
        my_maze = [start]
        neighbours = []

        for cell in start.neighbours:
            if not cell.reserved:
                neighbours.append((start, cell))

        while neighbours:
            cell, next_cell = random.choice(neighbours)
            neighbours.remove((cell, next_cell))
            if next_cell in my_maze:
                continue
            my_maze.append(next_cell)
            self.link_two(cell, next_cell, animate)
            for cell in next_cell.neighbours:
                if cell not in my_maze and not cell.reserved:
                    neighbours.append((next_cell, cell))
        if not perfect:
            self.unperfect(animate)

        if self.displayer:
            self.displayer.display_grid()

    def kuskal(self, perfect: bool, animate: bool=False) -> int:
        curses.curs_set(0)
        if self.seed == None:
            self.seed = random.randint(1000, 5000)
        random.seed(self.seed)
        all_links = [{cell} for rows in self.grid for cell in rows if not cell.reserved]

        while len(all_links) != 1:
            my_set = random.choice(all_links)
            actual = random.choice(list(my_set))
            unvisited = [cell for cell in actual.neighbours if not cell.reserved]
            if len(unvisited) < 2:
                continue
            chosen = random.choice(unvisited)
            unvisited.remove(chosen)
            if chosen in my_set:
                continue
            for cell in all_links:
                if chosen in cell:
                    my_set.update(cell)
                    all_links.remove(cell)
                    self.link_two(actual, chosen, animate)
                    break
        if not perfect:
            self.unperfect(animate)

        if self.displayer:
            self.displayer.display_grid()

    def link_two(self, cell_1: Cell, cell_2: Cell, animate: bool):
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
            self.displayer.update_cell_v1(cell_1)
            self.displayer.update_cell_v1(cell_2)
            time.sleep(0.02)
