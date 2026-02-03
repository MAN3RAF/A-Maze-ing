from mazegen.generate import MazeGenerator
from mazegen.display import ShowMaze
from mazegen.solve import switch_path, breadth_first_search
import curses
import sys
import os
from mazegen.parsing import parsing, ParsingError


def be_amazed(screen: curses.window) -> None:
    """
    Manage the initialisation of the maze, displayer, and user inputs
    
    :param screen: The screen given by the cursus.wrapper()
    it is on this window that we will draw the maze

    :type screen: curses.window
    """

    config = parsing(sys.argv[1])     # config dict

    # initialise the displayer, the maze and then initialise the maze inside the displayer
    display = ShowMaze(screen, config.get('seed'))
    maze = MazeGenerator(config['width'], config['height'],
                         config['entry'], config['exit'],
                         config.get('seed'), display)
    display.init_maze(maze)

    # display the maze and save it's seed inside the seed variable
    maze.backtracking(config['perfect'], True)

    # get the shortest path
    path = breadth_first_search(maze)

    while True:
        display.user_option()
        user_input = screen.getch()

        if user_input == ord('g'):    # static
            switch_path(path, display, animate=False, visible=False)    # clear path
            maze.init_maze()
            maze.prims(config['perfect'])
            path = breadth_first_search(maze)

        elif user_input == ord('a'):    # animated
            switch_path(path, display, animate=False, visible=False)    # clear path
            maze.init_maze()
            maze.prims(config['perfect'], True)
            path = breadth_first_search(maze)

        elif user_input == ord('c'):    # color
            display.switch_colors()
            display.display_grid()

        elif user_input == ord('f'):    # mid
            display.switch_colors('mid')
            display.display_grid()

        elif user_input == ord('p'):    # solve with BFS
            switch_path(path, display, animate=True)    # clear path

        elif user_input == ord('s'):    # save
            maze.save_seed()

        elif user_input == ord('q'):    # quit
            break


if __name__ == "__main__":
    if len(sys.argv) == 2:
        try:
            curses.wrapper(be_amazed)
        except KeyboardInterrupt:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Leaving already?")
            print("See you soon :) (use 'q' next time btw)")
        except curses.error:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("This window is way too small for this size")
        except FileNotFoundError as e:
            print("No config file, No run!")
        except (ParsingError, ValueError) as e:
            print(e)
    else:
        print("The filename is the only accepted/needed argument")