*This project has been created as part of the 42 curriculum by aaliouan, lsebar*

Mazes are cool :) so with my teammate we made a mazegenerator


# Description
The objective of this project is to generate mazes... ok we'll add a little more \
What we understood after this project is that maze, can be described as paths.\
The path that you chose will be the one the user will take. And thankfully\
there aresome algorithms that do that job!

We implemented 3 of thems:
- Backtracking
- Prim's
- Kruskal

Each one of them have a unique way of tracing it's path.

You have 2 ways of using this project:

1. Playing around with the script.
    - Generating some mazes and watching the output.
    - Animating the generation.
    - Show/hide shortest path.
2. Using the project as a .whl package:
    - Using the maze output to build something new\
     no need to think about the generation now.


# Instructions

### To just play around with the script you can use in the terminal:
``` console
~$ make run
```

This will automatically build a venv and install dependencies in it.\
You can change the maze settings in the 'config.txt'\
Then you can run again the command to display

After you are done with the script you can use:
``` console
~$ make clean
```
To delete all artifacts and the venv

### If you want to use the project as a package, use:

install the package using:
```console
~$ pip install a_maze_ing-1.0.0.tar.gz
```
You can now access the classes and functions of the project like any built in python library\
cool isn't it :)

Here are some way of using it:
```python
    from mazegen.generator import MazeGenerator
    # mazegen is the pachage name, here are it's content :
    # mazegen:
    #     generator.py: MazeGenerator
    #     display.py: ShowMaze
    #     solve.py: breadth_first_search(), switch_path()
    #     cell.py: Cell
    # The rest is just parsing and helper


    # MazeGenerator(width, height, start, end, seed, display)
    # Start and height are tupple coordinate (need to be in the range of the maze)
    # seed and display are optionnal:
    #     seed let you remember a maze to regenerate it (bigger than 1 and last digit between 0 and 2)
    #     display is the displayer class (ShowMaze)
    generator = MazeGenerator(10, 10, (0,0), (9,9))

    # There are different algorithms available:
    #     backtracking(perfect, displaying: bool, animate: bool) -> None:
    #     prims(perfect: bool, displaying: bool, animate: bool) -> None:
    #     kruskal(perfect: bool, displaying: bool, animate: bool) -> None:
    # Perfect will dictate whether the maze will be perfect or not (only one path)
    # display and animate are False by defalt.
    # display to show to maze, animate to display cell by cell
    generator.backtracking(True)

    # grid store the maze
    maze: list[list[Cell]] = generator.grid

    # path store the shortest path from entry to exit
    path: list[Cell] = generator.path

    # Save the maze structure in hexa format, entry, exit and path in the file
    generator.save_maze("output_file.txt")

    # More informations in the functions and class documentation
```


# Resources

Here are some helpful ressources that we used:
- [Wikipedia about maze generation](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Curses documentation](https://docs.python.org/3/howto/curses.html)
- [Geekforgeeks](https://www.geeksforgeeks.org/) for algorithm comprehension

Ressources we wish we knew earlier:
- [small book](https://www.cs.cmu.edu/~112-n23/notes/student-tp-guides/Mazes.pdf) about the fundamental of maze generation

### AI using
We used AI for this project mainly for:
- python syntax/concept:\
Learning new built in command\
Going deeper in some concept
- help for twisting algorithm (mainly Kruskal)

# Additional guideline

### Config file
- the config file structure need to be as follow:
```text
WIDTH=8
HEIGHT=7
ENTRY=0,0
EXIT=6,6
OUTPUT_FILE=output.txt
PERFECT=False
SEED=300
```
- You can comment seed by writing '#' before the line to ignore it\
- You can't comment the other mandatory keys
- width and height need to be positive int
- entry and exit need to be tupple in the range of the maze's scope
- output_file need to be a .txt
- perfect need to be a bool (True/False)
- seed need to be a positive int with it's last digit between 0 and 2

### Algos
like we've explained above.
1. We used 3 different algorithms for the maze generation:
    - Backtracking: Favorite one, it output a very natural and nice looking maze + animation
    - Prime's: Look like cells are spreading in the maze, nice to see
    - Kruskal: top 1 for the originality, cells doesn't spread, it apprear from nowhere.\
    Also the hardest to implement because of the code structure, we were tracking\
    cells not walls, so we twisted the algo a little bit. 

2. For the path finding we implemented only 1 (BFS) because of it's efficiency.
    - Breadth first search (BFS): Store in a dict {child: parent} the relation between\
    a cell and it's closest parent.

More information in the code docs

### What could be better

Well a group project is fundamentally different than working alone, we weren't really prepared\
for that, and we lost a lot of time because we started coding early. The tasks were not properly\
reparted too... But it is better to learn that now! thankfully we now understand all that\
and we will surely do better next time!
