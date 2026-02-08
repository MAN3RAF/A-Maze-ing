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
                curses.init_pair(1, c1, c2)
                curses.init_pair(2, c1, c3)
                curses.init_pair(3, c1, c4)
                curses.init_pair(4, c1, c5)
                curses.init_pair(5, c1, c6)
                return
            available = list(set(self.color_palet) - set(self.colors.values()))

            if element == "mid":
                self.colors['mid_back'] = random.choice(available)
                curses.init_pair(2, self.colors['walls'],
                                 self.colors['mid_back'])
            else:
                c1, c2, c3, c4, c5 = random.sample(available, 5)
                self.colors['walls'] = c1
                self.colors['maze_back'] = c2
                self.colors['path_back'] = c3
                self.colors['entry'] = c4
                self.colors['exit'] = c5
                curses.init_pair(1, c1, c2)
                curses.init_pair(2, c1, self.colors['mid_back'])
                curses.init_pair(3, c1, self.colors['path_back'])
                curses.init_pair(4, c1, self.colors['entry'])
                curses.init_pair(5, c1, self.colors['exit'])
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
            self.screen.addstr("3: kruskal algrotithm        <---\n")
        self.screen.move(maze.height * 2 + 5, 0)
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
        col = 1
        # Change the color pair to use based on the nature of the cell
        if cell.reserved:
            col = 2
        elif cell == maze.grid[maze.start[1]][maze.start[0]]:
            col = 4
        elif cell == maze.grid[maze.end[1]][maze.end[0]]:
            col = 5
        elif cell.path:
            col = 3

        draw_x = cell.x * 4
        draw_y = cell.y * 2
        top = False
        if cell.x > 0:
            # Does the top cell have a north wall or not
            if any(n.x == cell.x - 1
                   and n.walls['north'] for n in cell.neighbours):
                top = True
        self.screen.move(draw_y, draw_x)
        for i in range(2):
            # Size of cell = 4x2
            if cell.walls['west']:
                self.add("█", col)
            # Display the little block top only if
            # there is a wall on top or the left cell have a top wall
            elif (i == 0 and not cell.reserved
                  and (cell.walls['north'] or top)):
                self.add('▀', col)
            else:
                self.add(" ", col)

            if cell.walls['north'] and i == 0:
                self.add("▀▀▀", col)
            elif i == 0:
                self.add("   ", col)

            if i > 0:
                self.add("   ", col)

            if cell.x == maze.width - 1:
                # Border left
                self.add("█", col)

            draw_y += 1
            self.screen.move(draw_y, draw_x)
        if cell.y == maze.height - 1:
            # Border bottom
            self.screen.move(draw_y - 1, draw_x)
            if cell.walls['west']:
                self.add("█▄▄▄", col)
            else:
                self.add("▄▄▄▄", col)
        if animate:
            self.screen.refresh()
