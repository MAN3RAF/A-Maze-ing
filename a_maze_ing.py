from mazegen.generate import MazeGenerator
from mazegen.display import ShowMaze
from mazegen.solve import switch_path
import curses
import sys
import os
from mazegen.parsing import parsing, ParsingError, ParsingResult


def be_amazed(screen: curses.window, config: ParsingResult) -> None:
    """
    Manage the initialisation of the maze, displayer, and user inputs

    Args:
        screen (curses.window): The screen given by the cursus.wrapper().
                                The maze will be drawn there
        config (ParsingResult):
    """

    curses.curs_set(0)
    # initialise the displayer and the maze generator.

    display = ShowMaze(screen, config.get('seed'))
    maze = MazeGenerator(config['width'], config['height'],
                         config['entry'], config['exit'],
                         config.get('seed'), display)

    # generate and display the maze
    maze.apply_algo(config['perfect'], True, True)

    # save the maze to the file given by the user
    maze.save_maze(config['output_file'])

    while True:
        maze.user_option()
        user_input = screen.getch()

        # move player (entry)
        if user_input == curses.KEY_UP:
            maze.move_entry(0, -1)
        elif user_input == curses.KEY_DOWN:
            maze.move_entry(0, 1)
        elif user_input == curses.KEY_LEFT:
            maze.move_entry(-1, 0)
        elif user_input == curses.KEY_RIGHT:
            maze.move_entry(1, 0)

        # user algo choice
        elif user_input == ord('1'):
            maze.algo = 0
        elif user_input == ord('2'):
            maze.algo = 1
        elif user_input == ord('3'):
            maze.algo = 2

        elif user_input == ord('g'):    # static generation
            # clear path
            switch_path(maze.path, maze, animate=False, visible=False)
            maze.apply_algo(config['perfect'], True)
            maze.save_maze(config['output_file'])

        elif user_input == ord('a'):    # animated generation
            # clear path
            switch_path(maze.path, maze, animate=False, visible=False)
            maze.displayer.display_grid(maze)
            maze.apply_algo(config['perfect'], True, True)
            maze.save_maze(config['output_file'])

        elif user_input == ord('c'):    # change color
            maze.displayer.switch_colors()
            maze.displayer.display_grid(maze)

        elif user_input == ord('f'):    # change mid color
            maze.displayer.switch_colors('mid')
            maze.displayer.display_grid(maze)

        elif user_input == ord('p'):    # show/hide path
            if maze.path_visible is False:
                maze.path_visible = True
            else:
                maze.path_visible = False
            switch_path(maze.path, maze, animate=True)

        elif user_input == ord('s'):    # save
            maze.save_seed()

        elif user_input == ord('q'):    # quit
            break


if __name__ == "__main__":
    if len(sys.argv) == 2:    # Check the presence of 1 argument (filename)
        try:
            config = parsing(sys.argv[1])    # config = parsed user input
            curses.wrapper(be_amazed, config)
        except KeyboardInterrupt:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Leaving already?")
            print("See you soon :) (use 'q' next time btw)")
        except curses.error:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("This window is way too small for this size")
        except FileNotFoundError:
            print("No config file, No run!")
        except PermissionError:
            print("Can't access the file, permission denied, "
                  "check permission of:")
            print("config.txt")
            print("seed.txt   <-- if generated")
            print("output.txt <-- if generated")
        except (ParsingError, ValueError) as e:
            print(e)
    else:
        print("The filename is the only accepted/needed argument")
