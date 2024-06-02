
from random import randint
from battleship_game_functions import MIN_SHIP_SIZE, MAX_SHIP_SIZE, \
                                      MAX_GRID_SIZE, EMPTY, UNKNOWN
from battleship_game_functions import valid_cell_indexes, is_not_given_symbol


# helper functions for making a fleet grid for the computer

def make_empty_fleet_grid(grid_size: int) -> list[list[str]]:
    """Return a grid_size by grid_size grid containing EMPTY in every cell.

    Preconditions:
        - 1 <= grid_size <= MAX_GRID_SIZE

    >>> grid_1x1 = make_empty_fleet_grid(1)
    >>> grid_1x1 == [[EMPTY]]
    True
    >>> grid_2x2 = make_empty_fleet_grid(2)
    >>> grid_2x2 == [[EMPTY, EMPTY], [EMPTY, EMPTY]]
    True
    """

    fleet_grid = []
    for _ in range(grid_size):
        grid_row = [EMPTY] * grid_size
        fleet_grid.append(grid_row)
    return fleet_grid


def is_occupied(row1: int, col1: int, row2: int, col2: int,
                fleet_grid: list[list[str]]) -> bool:
    """Return True if and only if a cell between (row1, col1) and
    (row2, col2), inclusive, in fleet_grid is not set to the EMPTY symbol.

    Preconditions:
        - 0 <= row1 < len(fleet_grid) and 0 <= row2 < len(fleet_grid)
        - 0 <= col1 < len(fleet_grid) and 0 <= col2 < len(fleet_grid)
        - row1 == row2 or col1 == col2
        - 1 <= len(fleet_grid) <= MAX_GRID_SIZE
        - len(fleet_grid[i]) == len(fleet_grid)
              for each value of i in range(len(fleet_grid))

    >>> grid = make_empty_fleet_grid(3)
    >>> is_occupied(1, 1, 1, 2, grid)
    False
    >>> grid[1][1] = 'd'
    >>> is_occupied(1, 1, 1, 2, grid)
    True
    """

    if col1 == col2:
        for row in range(min(row1, row2), max(row1, row2) + 1):
            if fleet_grid[row][col1] != EMPTY:
                return True
    else:
        for col in range(min(col1, col2), max(col1, col2) + 1):
            if fleet_grid[row1][col] != EMPTY:
                return True

    return False


def get_end_indexes(start_row: int, start_col: int, ship_size: int) \
                    -> list[int]:
    """Return the end row and end column based on start_row, start_col, and
    ship_size, for a randomly generated direction.
    
    Note: the end row and end column could be outside of a grid.

    Preconditions:
        - 0 <= start_row < MAX_GRID_SIZE
        - 0 <= start_col < MAX_GRID_SIZE
        - MIN_SHIP_SIZE <= ship_size <= MAX_SHIP_SIZE

    (Examples not included since function depends on randomness.)
    """

    # randomly determine whether to place horizontally or vertically
    direction = randint(0, 1)

    if direction == 0:
        # calculate the (row, col) indexes for horizontal placement
        end_row = start_row
        end_col = start_col + ship_size - 1
    else:
        # calculate the (row, col) indexes for vertical placement
        end_row = start_row + ship_size - 1
        end_col = start_col

    return [end_row, end_col]


def place_ship(row1: int, col1: int, row2: int, col2: int,
               fleet_grid: list[list[str]], ship_symbol: str) -> None:
    """Modify fleet_grid by placing a ship_symbol from (row1, col1) to
    (row2, col2), inclusive.

    Preconditions:
        - 0 <= row1 <= row2 < len(fleet_grid)
        - 0 <= col1 <= col2 < len(fleet_grid)
        - row1 == row2 or col1 == col2
        - 1 <= len(fleet_grid) <= MAX_GRID_SIZE
        - len(fleet_grid[i]) == len(fleet_grid)
              for each value of i in range(len(fleet_grid))
        - len(ship_symbol) == 1

    >>> grid = make_empty_fleet_grid(3)
    >>> place_ship(0, 0, 1, 0, grid, 'd')
    >>> f_g = [['d', EMPTY, EMPTY], ['d', EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
    >>> grid == f_g
    True
    >>> place_ship(0, 1, 0, 2, grid, 'a')
    >>> f_g = [['d', 'a', 'a'], ['d', EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
    >>> grid == f_g
    True
    """

    if row1 == row2:
        # place the ship horizontally
        for col in range(col1, col2 + 1):
            fleet_grid[row1][col] = ship_symbol
    else:
        # place the ship vertically
        for row in range(row1, row2 + 1):
            fleet_grid[row][col1] = ship_symbol


def randomly_place_ship(fleet_grid: list[list[str]], ship_symbol: str,
                        ship_size: int) -> bool:
    """Return True if and only if a random attempt to place ship using 
    ship_symbol with ship_size in fleet_grid was successful.

    Preconditions:
        - 1 <= len(fleet_grid) <= MAX_GRID_SIZE
        - len(fleet_grid[i]) == len(fleet_grid)
              for each value of i in range(len(fleet_grid))
        - len(ship_symbol) == 1
        - MIN_SHIP_SIZE <= ship_size <= MAX_SHIP_SIZE

    (Examples not included since function depends on randomness.)
    """

    grid_size = len(fleet_grid)

    # randomly generate a location at which to place the ship
    start_row = randint(0, grid_size - 1)
    start_col = randint(0, grid_size - 1)

    ends = get_end_indexes(start_row, start_col, ship_size)
    end_row = ends[0]
    end_col = ends[1]

    # If the start and end locations are within the bounds of the grid
    # and the cells are not already occupied, place the ship.
    if valid_cell_indexes(start_row, start_col, grid_size) \
       and valid_cell_indexes(end_row, end_col, grid_size) \
       and not is_occupied(start_row, start_col, end_row, end_col, fleet_grid):
        place_ship(start_row, start_col, end_row, end_col,
                   fleet_grid, ship_symbol)
        return True

    return False


# The following two functions are called in the play_battleship_game module
# to set up the computer's fleet grid and to make the computer's guess.

def generate_fleet_grid(grid_size: int, ship_symbols: list[str],
                        ship_sizes: list[int]) -> list[list[str]]:
    """Return a new grid_size by grid_size fleet grid using the ship symbols
    in ship_symbols and the corresponding ship sizes in ship_sizes.  Ships are
    placed randomly on the fleet grid, horizontally and/or vertically, and the
    rest of the cells contain the EMPTY symbol.

    Preconditions:
        - 1 <= grid_size <= MAX_GRID_SIZE
        - len(ship_symbols) == len(ship_sizes)
        - len(ship_symbols[i]) == 1
              for each value of i in range(len(ship_symbols))
        - ship_symbols[i] is unique
              for each value of i in range(len(ship_symbols))
        - MIN_SHIP_SIZE <= ship_sizes[i] <= MAX_SHIP_SIZE
              for each value of i in range(len(ship_sizes))

    (Examples not included since function depends on randomness.)
    """

    fleet_grid = make_empty_fleet_grid(grid_size)

    for index in range(len(ship_symbols) - 1, -1, -1):
        # get the ship symbol and its size
        ship = ship_symbols[index]
        ship_size = ship_sizes[index]

        placed = False

        # This produces an infinite loop when a ship is too big to be placed.
        # Would be best to place ships by size, with biggest first.
        while not placed:
            placed = randomly_place_ship(fleet_grid, ship, ship_size)

    return fleet_grid


def make_computer_guess(target_grid: list[list[str]]) -> list[int]:
    """Return row and column indexes for a randomly chosen UNKNOWN cell in the
    target_grid to use as the computer's next guess.

    Preconditions:
        - 1 <= len(target_grid) <= MAX_GRID_SIZE
        - len(target_grid[i]) == len(target_grid)
              for each value of i in range(len(target_grid))

    (Examples not included since function depends on randomness.)
    """

    grid_size = len(target_grid)

    # generate random grid positions until the value of the target_grid cell
    # at the position is UNKNOWN
    row = randint(0, grid_size - 1)
    col = randint(0, grid_size - 1)
    while is_not_given_symbol(row, col, target_grid, UNKNOWN):
        row = randint(0, grid_size - 1)
        col = randint(0, grid_size - 1)

    return [row, col]


if __name__ == '__main__':
    # Automatically run all doctest examples to see if any fail
    import doctest
    # uncomment the line below to run the docstring examples
    doctest.testmod()
