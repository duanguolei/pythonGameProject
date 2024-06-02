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
        # # print(lines)
        # print(maze)
        # print(player_stats)

    return maze, player_stats


class SokobanView:
    """ A simple text-based view for Fancy Sokoban. """
    def display_game(
        self,
        maze: Grid,
        entities: Entities,
        player_position: Position
    ) -> None:
        """ Display the current state of the game.
        
        Parameters:
            maze: The current maze.
            entities: A dictionary mapping positions to entities
            player_position: The current position of the player.
        """
        for i, row in enumerate(maze):
            for j, tile in enumerate(row):
                if (i, j) == player_position:
                    print(PLAYER, end='')
                else:
                    print(entities.get((i, j), tile), end='')
            print()
        print()

    def display_stats(self, moves_remaining: int, strength: int) -> None:
        """ Display the current stats of the player.
        
        Parameters:
            moves_remaining: The number of moves the player has remaining.
            strength: The current strength of the player.
        """
        print(f'Moves remaining: {moves_remaining}, strength: {strength}\n')
