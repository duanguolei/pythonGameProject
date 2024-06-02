Grid = list[list['Tile']]
Entities = dict[tuple[int, int], 'Entity']
Position = tuple[int, int]

# Tile constants
WALL = 'W'
FLOOR = ' '
GOAL = 'G'
FILLED_GOAL = 'X'

# Entity constants
CRATE = 'C'
PLAYER = 'P'
STRENGTH_POTION = 'S'
MOVE_POTION = 'M'
FANCY_POTION = 'F'

# Movement constants
UP = 'w'
DOWN = 's'
LEFT = 'a'
RIGHT = 'd'

DIRECTION_DELTAS = {
    UP: (-1, 0),
    DOWN: (1, 0),
    LEFT: (0, -1),
    RIGHT: (0, 1),
}


def read_file(maze_file: str) -> tuple[list[list[str]], list[int, int]]:
    """ A helper function to read maze files into a basic format.

    Parameters:
        maze_file: The path to the maze file (e.g. 'maze_files/maze1.txt')

    Returns:
        A tuple containing two items:
            1) A simple representation of the maze
            2) A list containing the starting values for the player's strength
               and moves remaining respectively.
    """
    with open(maze_file, 'r') as file:
        lines = file.readlines()
        maze = [list(line.strip()) for line in lines[1:]]
        player_stats = [int(item) for item in lines[0].strip().split(' ')]

    return maze, player_stats
