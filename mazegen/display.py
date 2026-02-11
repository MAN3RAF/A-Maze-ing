import curses
import random
from mazegen.cell import Cell
from mazegen.generate import MazeGenerator


class ShowMaze:
    """
    Render maze generation/solving progress to a curses screen.

    Args:
        screen (curses.window): Screen to display on
        colorist (ColorManager): Manage colors

    Inner Class:
        ColorManager: Store and manage the colors of each maze's elements

    Methods:
        switch_colors(): Call ColorManager().switch_colors()
        user_options(): Display user options
        display_grid(): Display the entire grid
        update_cell(): Display/update the cell given in parameter
    """

    class ColorManager:
        """
        Manage color pairs for different maze elements.

        Args:
            colors (dict[str, int]): Store the color of each element.
            color_palet (list[int]): Store available colors.

        Methods:
            switch_colors(element: str): switch color of the maze or the mid
        """

        def __init__(self, seed: int | None) -> None:
            """
            Initialize color palette

            Args:
                seed (Optionnal[int]): Optionally seeding randomness.
            """
            curses.start_color()
            curses.use_default_colors()
            self.colors: dict[str, int] = {}
            if curses.COLORS == 256:
                self.color_palet: list[int] = [i for i in range(255)]
            else:
                self.color_palet = [curses.COLOR_WHITE,
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

        def switch_colors(self, element: str = "maze") -> None:
            """
            Rotate colors for the full maze or only some parts of it.

            Args:
                element (str): Element to change
            """
            if not self.colors:
                # initialise colors if colors is empty
                c1, c2, c3, c4, c5, c6 = random.sample(self.color_palet, 6)
                self.colors.update({
                    'walls': c1,
                    'maze_back': c2,
                    'mid_back': c3,
                    'path_back': c4,
                    'entry': c5,
                    'exit': c6
                    }
                    )
                # base colors
                curses.init_pair(1, c1, c2)
                curses.init_pair(2, c1, c3)
                curses.init_pair(3, c1, c4)
                curses.init_pair(4, c1, c5)
                curses.init_pair(5, c1, c6)

                # additionnal edge cases colors
                curses.init_pair(6, c1, -1)
                curses.init_pair(7, c2, c5)
                curses.init_pair(8, c2, c6)
                curses.init_pair(9, c2, c4)
                curses.init_pair(11, c4, c6)
                curses.init_pair(10, c4, c5)
                return
            available = list(set(self.color_palet) - set(self.colors.values()))

            if element == "mid":
                self.colors['mid_back'] = random.choice(available)
                curses.init_pair(2, self.colors['walls'],
                                 self.colors['mid_back'])
            else:
                c1, c2, c4, c5, c6 = random.sample(available, 5)
                self.colors['walls'] = c1
                self.colors['maze_back'] = c2
                self.colors['path_back'] = c4
                self.colors['entry'] = c5
                self.colors['exit'] = c6
                # base colors
                curses.init_pair(1, c1, c2)
                curses.init_pair(2, c1, self.colors['mid_back'])
                curses.init_pair(3, c1, self.colors['path_back'])
                curses.init_pair(4, c1, self.colors['entry'])
                curses.init_pair(5, c1, self.colors['exit'])

                # additionnal edge case colors
                curses.init_pair(6, c1, -1)
                curses.init_pair(7, c2, c5)
                curses.init_pair(8, c2, c6)
                curses.init_pair(9, c2, c4)
                curses.init_pair(11, c4, c6)
                curses.init_pair(10, c4, c5)
                return

    def __init__(self, screen: curses.window,
                 seed: int | None = None) -> None:
        """
        Initialize the maze renderer with a curses screen and color seed.

        Args:
            screen (curses.window): Screen to display on
            colorist (ColorManager): Manage colors
        """
        self.screen = screen
        self.colorist = self.ColorManager(seed)

    def switch_colors(self, element: str = "maze") -> None:
        """Delegate color cycling to the helper color manager."""
        self.colorist.switch_colors(element)

    def user_option(self, maze: MazeGenerator) -> None:
        """Print the interactive help legend under the rendered maze."""
        self.screen.move(maze.height * 2 + 1, 0)
        self.screen.addstr("\nchoose the algo then use "
                           "'g' or 'a' to generate\n\n")
        if maze.algo == 0:
            self.screen.addstr("1: Backtracking algorithm   <---\n")
            self.screen.addstr("2: Prim's algorithm\n")
            self.screen.addstr("3: kruskal algrotithm\n")
        elif maze.algo == 1:
            self.screen.addstr("1: Backtracking algorithm\n")
            self.screen.addstr("2: Prim's algorithm         <---\n")
            self.screen.addstr("3: kruskal algrotithm\n")
        elif maze.algo == 2:
            self.screen.addstr("1: Backtracking algorithm\n")
            self.screen.addstr("2: Prim's algorithm\n")
            self.screen.addstr("3: kruskal algrotithm       <---\n")

        self.screen.move(maze.height * 2 + 8, 0)
        self.screen.addstr("↑: move up\n")
        self.screen.addstr("↓: move down\n")
        self.screen.addstr("←: move left\n")
        self.screen.addstr("→: move right\n")
        self.screen.addstr("g: static maze generation\n")
        self.screen.addstr("a: animated maze generation\n")
        self.screen.addstr("c: change maze color\n")
        self.screen.addstr("f: change 42 style\n")
        self.screen.addstr("p: solve maze (BFS)\n")
        self.screen.addstr("s: Save maze seed to .txt file\n")
        self.screen.addstr("q: quit\n")

    def add(self, text: str, c: int) -> None:
        """Write 'text' with the given color pair index 'c'."""
        self.screen.addstr(text, curses.color_pair(c))

    def display_grid(self, maze: MazeGenerator) -> None:
        """Render an entire maze at once without animations."""
        self.screen.clear()
        self.screen.move(0, 0)
        for rows in maze.grid:
            for cell in rows:
                self.update_cell(cell, maze, animate=False)
        self.screen.refresh()

    def update_cell(self, cell: Cell, maze: MazeGenerator,
                    animate: bool = True) -> None:
        """
        Redraw a single cell, optionally refreshing the screen immediately.

        cell (Cell): Cell to display
        maze (MazeGenerator): The maze (for entry, exit, size etc..)
        animate (bool): Whether to refresh screen immediately
        """
        # Condition to display a little block on top
        corner = False
        if (cell.walls['north'] or
                any((n.x == cell.x - 1 and n.walls['north']) or
                    (n.y == cell.y - 1 and n.walls['west'])
                    for n in cell.neighbours)):
            corner = True

        if cell == maze.grid[maze.start[1]][maze.start[0]]:
            self.draw_special(cell, maze, 8, corner)
            return
        elif cell == maze.grid[maze.end[1]][maze.end[0]]:
            self.draw_special(cell, maze, 7, corner)
            return

        col = 1
        # Change the color pair to use based on the nature of the cell
        if cell.reserved:
            col = 2

        elif cell.path:
            col = 3

        # Size of cell = 4x2
        draw_x = cell.x * 4
        draw_y = cell.y * 2

        # Build the two rows as strings
        rows = []
        for i in range(2):
            # Store here, display later at once
            line = []

            if cell.walls['west']:
                line.append(("█", col))
            elif i == 0 and not cell.reserved and corner:
                # path or not
                if (cell.path and cell.x > 0
                        and not maze.grid[cell.y][cell.x - 1].path):
                    line.append(("▀", 1))
                else:
                    line.append(("▀", col))
            else:
                # path or not
                if (cell.path and cell.x > 0
                        and not maze.grid[cell.y][cell.x - 1].path):
                    line.append((" ", 1))
                elif cell.path and i == 0:
                    line.append(("▀", 9))
                else:
                    line.append((" ", col))

            if i == 0:
                if cell.walls['north']:
                    line.append(("▀▀▀", col))
                else:
                    # path or not
                    if (cell.path and cell.y > 0
                            and not maze.grid[cell.y - 1][cell.x].path):
                        line.append(("▀▀▀", 9))
                    else:
                        line.append(("   ", col))
            else:
                line.append(("   ", col))

            if cell.x == maze.width - 1:
                line.append(("█", col))

            rows.append(line)

        # Draw rows at once (no multiple calls)
        for i, row in enumerate(rows):
            self.screen.move(draw_y + i, draw_x)
            for ch, color in row:
                self.add(ch, color)

        # Border bottom
        if cell.y == maze.height - 1:
            self.screen.move(draw_y + 2, draw_x)
            self.add("▀▀▀▀▀", 6)

        if animate:
            self.screen.refresh()

    def draw_special(self, cell: Cell, maze: MazeGenerator, col: int,
                     corner: bool) -> None:
        """
        Handling edge cases with entry exit and path

        cell (Cell): Cell to process
        maze (MazeGenerator): The maze to access the grid
        col (int): the color to base on the cell
        """
        color: int
        draw_x = cell.x * 4
        draw_y = cell.y * 2

        if cell.walls['west']:
            self.screen.addstr(draw_y, draw_x, "█",
                               curses.color_pair(1))
            self.screen.addstr(draw_y + 1, draw_x, "█",
                               curses.color_pair(1))
        else:
            # Is there a path on left or background color
            color = (3 if cell.x > 0 and maze.grid[cell.y][cell.x - 1].path
                     else 1)
            if corner:
                self.screen.addstr(draw_y, draw_x, "▀",
                                   curses.color_pair(color))
            else:
                self.screen.addstr(draw_y, draw_x, " ",
                                   curses.color_pair(color))
            self.screen.addstr(draw_y + 1, draw_x, " ",
                               curses.color_pair(color))

        if cell.walls['north']:
            self.screen.addstr(draw_y, draw_x + 1, "▀▀▀",
                               curses.color_pair(col - 3))
        else:
            # Is there a path on top or background color
            color = (1 if cell.y > 0 and maze.grid[cell.y - 1][cell.x].path
                     else 0)
            if color:
                self.screen.addstr(draw_y, draw_x + 1, "▀▀▀",
                                   curses.color_pair(col + 3))
            else:
                self.screen.addstr(draw_y, draw_x + 1, "▀▀▀",
                                   curses.color_pair(col))

        # Middle section
        self.screen.addstr(draw_y + 1, draw_x + 1, "   ",
                           curses.color_pair(col))

        if cell.x == maze.width - 1:
            # Border right
            self.screen.addstr(draw_y, draw_x + 4, "█",
                               curses.color_pair(1))
            self.screen.addstr(draw_y + 1, draw_x + 4, "█",
                               curses.color_pair(1))

        if cell.y == maze.height - 1:
            # Border bottom
            self.screen.addstr(draw_y + 2, draw_x, "▀▀▀▀▀",
                               curses.color_pair(6))
