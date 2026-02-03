import curses
import random
from mazegen.cell import Cell


class ShowMaze:
    class ColorManager:
        def __init__(self, seed):
            curses.start_color()
            curses.use_default_colors()
            self.colors: dict = {}
            if curses.COLORS == 256:
                self.color_palet = [i for i in range(255)]
            else:
                self.color_palet: list = [curses.COLOR_WHITE,
                                          curses.COLOR_BLACK,
                                          curses.COLOR_BLUE,
                                          curses.COLOR_GREEN,
                                          curses.COLOR_MAGENTA,
                                          curses.COLOR_RED,
                                          curses.COLOR_YELLOW,
                                          curses.COLOR_CYAN]
            if seed:
                random.seed(seed)
            self.switch_colors()

        def switch_colors(self, element: str="maze") -> None:
            if not self.colors:
                c1, c2, c3, c4 = random.sample(self.color_palet, 4)
                self.colors.update({
                    'walls': c1,
                    'maze_back': c2,
                    'mid_back': c3,
                    'path_back': c4
                    }
                    )
                curses.init_pair(1, c1, c2)
                curses.init_pair(2, c1, c3)
                curses.init_pair(3, c1, c4)
                return
            available = list(set(self.color_palet) - set(self.colors.values()))

            if element == "mid":
                self.colors['mid_back'] = random.choice(available)
                curses.init_pair(2, self.colors['walls'],
                                 self.colors['mid_back'])
            else:
                c1, c2, c3 = random.sample(available, 3)
                self.colors['walls'] = c1
                self.colors['maze_back'] = c2
                self.colors['path_back'] = c3
                curses.init_pair(1, c1, c2)
                curses.init_pair(2, c1, self.colors['mid_back'])
                curses.init_pair(3, c1, self.colors['path_back'])
                return

    def __init__(self, screen: curses.window, seed: int=None) -> None:
        self.screen = screen
        self.colorist = self.ColorManager(seed)

    def init_maze(self, maze):
        self.maze = maze

    def switch_colors(self, element: str="maze"):
        self.colorist.switch_colors(element)

    def user_option(self) -> None:
        self.screen.move(self.maze.height * 3 + 5, 0)
        self.screen.addstr("g: generate static maze\n")
        self.screen.addstr("a: animated maze generation\n")
        self.screen.addstr("c: change maze color\n")
        self.screen.addstr("f: change 42 style\n")
        self.screen.addstr("p: solve maze (BFS)\n")
        self.screen.addstr("s: Save maze seed to .txt file\n")
        self.screen.addstr("q: quit\n")

    def add(self, str: str, c: int) -> None:
        self.screen.addstr(str, curses.color_pair(c))

    def display_grid(self) -> None:
        self.screen.clear()
        self.screen.move(0, 0)
        for rows in self.maze.grid:
            for cell in rows:
                self.update_cell_v1(cell, animate=False)
        self.screen.refresh()

    def update_cell_v1(self, cell: Cell, animate: bool=True) -> None:
        col = 1
        if cell.reserved:
            col = 2
        elif cell.path:
            col = 3
        draw_x = cell.x * 6
        draw_y = cell.y * 3
        top = False
        if cell.x > 0:
            if any(n.x == cell.x - 1 and n.walls['north'] for n in cell.neighbours):
                top = True
        self.screen.move(draw_y, draw_x)
        for i in range(3):
            if cell.walls['west']:
                self.add("█", col)
            elif i == 0 and not cell.reserved and (cell.walls['north'] or top):
                self.add('▀', col)
            else:
                self.add(" ", col)

            if cell.walls['north'] and i == 0:
                self.add("▀▀▀▀▀", col)
            elif i == 0:
                self.add("     ", col)

            if i > 0:
                self.add("     ", col)

            if cell.x == self.maze.width - 1:
                self.add("█", col)

            draw_y += 1
            self.screen.move(draw_y, draw_x)
        if cell.y == self.maze.height - 1:
            self.screen.move(draw_y - 1, draw_x)
            if cell.walls['west']:
                self.add("█▄▄▄▄▄", col)

            else:
                self.add("▄▄▄▄▄▄", col)
        if animate:
            self.screen.refresh()
