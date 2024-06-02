
import os
from typing import TextIO
from battleship_game_functions import MIN_SHIP_SIZE, MAX_SHIP_SIZE, \
                                      MAX_GRID_SIZE, UNKNOWN, EMPTY, HIT, MISS
from battleship_game_functions import valid_cell_indexes, \
                                      is_not_given_symbol, is_win, \
                                      update_target_grid, update_fleet_grid, \
                                      validate_symbol_counts, \
                                      validate_ship_positions
from computer_play_functions import generate_fleet_grid, make_computer_guess

# This code won't work until you've completed your functions in the
# battleship_game_functions module.
#
# Some functions that are called when playing the game follow.  Students may
# find it helpful to review and try to understand the code below these lines.
# Do NOT change any of it!

HIT_MESSAGE = 'hit a ship'
MISS_MESSAGE = 'missed'

# The following 4 functions are used to read a game layout from a file.

def read_game_file() -> list[list]:
    """Return the ship and symbol grid data from a game file whose file name
    was provided by the game user.
    
    The first item in the returned nested list is a list[str] (ship symbols).
    The second item in the returned nested list is a list[int] (the sizes of
      the corresponding ships in the first item.
    The third item in the returned nested list is a list[list[str]] (the
      player's fleet grid placements).

    (Examples not included since function depends on input and output.)
    """

    filename = get_valid_filename('\nEnter the name of a game file: ')
    game_file = open(filename)
    ships_data = read_ship_data(game_file)
    ship_symbols = ships_data[0]
    ship_sizes = ships_data[1]
    fleet_grid = read_fleet_grid(game_file)
    game_file.close()
    return [ship_symbols, ship_sizes, fleet_grid]


def get_valid_filename(msg: str) -> str:
    """Return the name of a file entered by the user when prompted with msg.

    A file with the entered file name should exist in the same folder as
    this file. Keep prompting the user until a valid file name is entered.

    (Examples not included since function depends on input and output.)
    """

    filename = input(msg)
    while not os.path.exists(filename):
        print('That file does not exist in this folder. Please try again.')
        filename = input(msg)

    return filename


def read_ship_data(game_file: TextIO) -> list[list]:
    """Return a list containing the ship symbols in game_file as a list of
    strings at index 0, and the ship sizes in game_file as a list of ints at
    index 1.

    The first item in the returned nested list is a list[str] (ship symbols).
    The second item in the returned nested list is a list[int] (the sizes of
      the corresponding ships in the first item.
      
    (Examples not included since function depends on input and output.)
    """

    ship_symbols = game_file.readline().strip().split()

    ship_sizes = game_file.readline().strip().split()
    for i in range(len(ship_sizes)):
        ship_sizes[i] = int(ship_sizes[i])

    return [ship_symbols, ship_sizes]


def read_fleet_grid(game_file: TextIO) -> list[list[str]]:
    """Return the fleet grid that is found in game_file.

    (Examples not included since function depends on input and output.)
    """

    fleet_grid = []
    for line in game_file:
        line = line.strip()
        sublist = []
        for char in line:
            sublist.append(char)
        fleet_grid.append(sublist)

    return fleet_grid


# The following 3 functions are used to validate game information that was read

def is_valid_game(fleet_grid: list[list[str]], ship_symbols: list[str],
                  ship_sizes: list[int]) -> bool:
    """Return True if and only if the game parameters fleet_grid, ship_symbols,
    and ship_sizes are valid, and fleet_grid is a valid grid.

    >>> grid = [[EMPTY, 'b', EMPTY], [EMPTY, 'b', EMPTY], ['a', 'a', 'a']]
    >>> ships = ['a', 'b']
    >>> sizes = [3, 2]
    >>> is_valid_game(grid, ships, sizes)
    True
    >>> grid = [['b', EMPTY, EMPTY], [EMPTY, 'b', EMPTY], ['a', 'a', 'a']]
    >>> ships = ['a', 'b']
    >>> sizes = [3, 2]
    >>> is_valid_game(grid, ships, sizes)
    False
    """

    return validate_game_parameters(fleet_grid, ship_symbols, ship_sizes) \
           and validate_fleet_grid(fleet_grid, ship_symbols, ship_sizes)


def validate_game_parameters(fleet_grid: list[list[str]],
                             ship_symbols: list[str],
                             ship_sizes: list[int]) -> bool:
    """Return True if and only if fleet_grid is square with at least one cell
    and at most MAX_GRID_SIZE cells per row, the number of ship symbols in
    ship_symbols is the same as the number of sizes in ship_sizes, that there
    is at least one ship, all ships have a valid size, and all ships have a
    valid, unique character label.

    >>> grid = [[EMPTY, 'b', EMPTY], [EMPTY, 'b', EMPTY], ['a', 'a', 'a']]
    >>> ships = ['a', 'b']
    >>> sizes = [3, 2]
    >>> validate_game_parameters(grid, ships, sizes)
    True
    >>> grid = []
    >>> ships = ['a', 'd', 'h', 'i', 'n']
    >>> sizes = [1, 1, 1, 2, 1]
    >>> validate_game_parameters(grid, ships, sizes)
    False
    """

    # Confirm that the fleet_grid has a valid number of rows.
    if len(fleet_grid) == 0 or len(fleet_grid) > MAX_GRID_SIZE:
        return False

    # Confirm that the fleet_grid is square.
    for row in fleet_grid:
        if len(row) != len(fleet_grid):
            return False

    # Confirm that number of ships is the same as the number of ship sizes.
    if len(ship_symbols) != len(ship_sizes):
        return False

    # Confirm that the ship_symbols and ship_sizes lists are not empty.
    if len(ship_symbols) == 0:
        return False

    # Confirm that each ship has a valid size.
    for size in ship_sizes:
        if size < MIN_SHIP_SIZE or size > MAX_SHIP_SIZE:
            return False

    # Confirm that each ship has a single-character label.
    for ship_symbol in ship_symbols:
        if len(ship_symbol) != 1:
            return False

    # Confirm that each ship has a unique label.
    for i in range(len(ship_symbols)):
        for j in range(len(ship_symbols)):
            if i != j and ship_symbols[i] == ship_symbols[j]:
                return False

    return True


def validate_fleet_grid(fleet_grid: list[list[str]],
                        ship_symbols: list[str],
                        ship_sizes: list[int]) -> bool:
    """Return True if and only if fleet_grid contains a ship of the correct
    size for each ship in ship_symbols and with the corresponding size from
    ship_sizes, and nothing else except for the EMPTY character.  Each ship in
    ship_symbols must also have a valid alignment (all symbols appearing across
    a row or down a column) in fleet_grid.

    Preconditions:
        - len(ships) == len(sizes) and 0 < len(ships)
        - 0 < len(fleet_grid)
        - len(fleet_grid[i]) == len(fleet_grid)
              for each value of i in range(len(fleet_grid))

    >>> my_grid = [[EMPTY, 'b', EMPTY], [EMPTY, 'b', EMPTY], ['a', 'a', 'a']]
    >>> my_ships = ['a', 'b']
    >>> my_sizes = [3, 2]
    >>> validate_fleet_grid(my_grid, my_ships, my_sizes)
    True
    >>> my_grid = [['d', 'a', 'n'], [EMPTY, 'i', 's'], ['f', 'i', 't']]
    >>> my_ships = ['a', 'd', 'f', 'i', 'n']
    >>> my_sizes = [1, 1, 1, 2, 1]
    >>> validate_fleet_grid(my_grid, my_ships, my_sizes)
    False
    """


    return validate_symbol_counts(fleet_grid, ship_symbols, ship_sizes) \
           and validate_ship_positions(fleet_grid, ship_symbols, ship_sizes)


# The following 2 functions set up and display the game

def get_target_grid(grid_size: int) -> list[list[str]]:
    """Return a grid_size by grid_size grid of UNKNOWN characters.

    >>> grid_1x1 = get_target_grid(1)
    >>> grid_1x1 == [[UNKNOWN]]
    True
    >>> grid_2x2 = get_target_grid(2)
    >>> grid_2x2 == [[UNKNOWN, UNKNOWN], [UNKNOWN, UNKNOWN]]
    True
    """

    target_grid = []
    for _ in range(grid_size):
        target_grid_row = [UNKNOWN] * grid_size
        target_grid.append(target_grid_row)
    return target_grid


def display_grids(target_grid: list[list[str]],
                  fleet_grid: list[list[str]]) -> None:
    """Display the target_grid and the fleet_grid that belong to a player.

    (Examples not included since function depends on input and output.)
    """

    print('\nMy target grid.               My fleet grid.\n')
    gap_between_grids = ' ' * (28 - len(target_grid))

    # Display the column numbers
    print(' ', end='')
    for col in range(len(target_grid)):
        print(col, end='')
    print(gap_between_grids + ' ', end='')
    for col in range(len(target_grid)):
        print(col, end='')
    print()

    # Display row numbers and cell contents.
    for row in range(len(target_grid)):
        print(row, end='')
        for col in range(len(target_grid)):
            print(target_grid[row][col], end='')
        print(gap_between_grids + str(row), end='')
        for col in range(len(fleet_grid)):
            print(fleet_grid[row][col], end='')
        print()

    print()
    print(' ' + HIT + ' means hit,                Upper-case means hit.')
    print(' ' + MISS + ' means miss.')


# The following 3 functions help play the game by getting and making moves

def get_row_col() -> list[int]:
    """Return the row and column indexes entered by the user when prompted.

    (Examples not included since function depends on input and output.)
    """

    row = input('Please enter the row: ')
    col = input('Please enter the column: ')
    if row.isdigit() and col.isdigit():
        row = int(row)
        col = int(col)
    else:
        row = -1
        col = -1

    return [row, col]


def get_valid_player_move(target_grid: list[list[str]]) -> list[int]:
    """Return a two item list that contains the player's move.

    (Examples not included since function depends on input and output.)
    """

    grid_size = len(target_grid)

    # Get initial move
    [row, col] = get_row_col()

    # Keep asking until user enters valid move
    while (not valid_cell_indexes(row, col, grid_size) or
               is_not_given_symbol(row, col, target_grid, UNKNOWN)):
        print('Invalid move! Either already known or invalid indexes! \n')
        [row, col] = get_row_col()

    return [row, col]


def make_move(row: int, col: int, fleet_grid: list[list[str]],
              ship_symbols: list[str], hits_list: list[int],
              target_grid: list[list[str]]) -> str:
    """Return HIT_MESSAGE and update hits_list and fleet_grid, using
    ship_symbols, if there is a ship at row and col, or return MISS_MESSAGE if
    there is no ship at row and col.  Update target_grid in both cases.

    >>> hits_list = [0]
    >>> fleet_grid = [[EMPTY, 'a'], [EMPTY, 'a']]
    >>> target_grid = [[UNKNOWN, UNKNOWN], [UNKNOWN, UNKNOWN]]
    >>> r = make_move(0, 0, fleet_grid, ['a'], hits_list, target_grid)
    >>> r == MISS_MESSAGE
    True
    >>> hits_list
    [0]
    >>> expected_fleet_grid = [[EMPTY, 'a'], [EMPTY, 'a']]
    >>> fleet_grid == expected_fleet_grid
    True
    >>> expected_target_grid = [[MISS, UNKNOWN], [UNKNOWN, UNKNOWN]]
    >>> target_grid == expected_target_grid
    True
    >>> r = make_move(0, 1, fleet_grid, ['a'], hits_list, target_grid)
    >>> r == HIT_MESSAGE
    True
    >>> hits_list
    [1]
    >>> expected_fleet_grid = [[EMPTY, 'A'], [EMPTY, 'a']]
    >>> fleet_grid == expected_fleet_grid
    True
    >>> expected_target_grid = [[MISS, HIT], [UNKNOWN, UNKNOWN]]
    >>> target_grid == expected_target_grid
    True
    """

    if is_not_given_symbol(row, col, fleet_grid, EMPTY):
        update_fleet_grid(row, col, fleet_grid, ship_symbols, hits_list)
        update_target_grid(row, col, target_grid, fleet_grid)
        return HIT_MESSAGE
    else:
        update_target_grid(row, col, target_grid, fleet_grid)
        return MISS_MESSAGE


def get_num_moves(target_grid: list[list[str]]) -> int:
    """Return the number of moves made so far for the board target_grid, based
    on the number of non-UNKNOWN elements.

    >>> get_num_moves([[UNKNOWN, UNKNOWN], [UNKNOWN, UNKNOWN]])
    0
    >>> get_num_moves([[UNKNOWN, 'M'], ['X', UNKNOWN]])
    2
    """

    moves_count = 0
    for row in target_grid:
        for symbol in row:
            if symbol != UNKNOWN:
                moves_count = moves_count + 1

    return moves_count


# The following two different functions may be used to play either a single
# player game (player against themself) or a game versus a computer opponent.

def play_single_player() -> None:
    """A single player game with no opponent. This may be used for the purpose
    of testing our functions.

    (Examples not included since function depends on input and output.)
    """

    # Read the game file
    ship_symbols, ship_sizes, fleet_grid = read_game_file()

    # Make sure the game is valid
    if not is_valid_game(fleet_grid, ship_symbols, ship_sizes):
        print('The supplied game is not valid.  Game exiting.')
        return

    # Set up the game
    target_grid = get_target_grid(len(fleet_grid))
    display_grids(target_grid, fleet_grid)
    hits_list = [0] * len(ship_sizes)

    # Play the game until it's over
    while not is_win(ship_sizes, hits_list):

        print('\nTake a turn.')
        [row, col] = get_valid_player_move(target_grid)
        print()

        message = make_move(row, col, fleet_grid, ship_symbols,
                            hits_list, target_grid)
        print(f'You {message}!')

        if is_not_given_symbol(row, col, fleet_grid, EMPTY):
            ship_index = ship_symbols.index(fleet_grid[row][col].lower())
            if hits_list[ship_index] >= ship_sizes[ship_index]:
                ship_size = ship_sizes[ship_index]
                ship_symbol = ship_symbols[ship_index]
                print(f'The size {ship_size} {ship_symbol} ship ' \
                       'has been sunk!')

        display_grids(target_grid, fleet_grid)

    # Game is over, display results
    print(f'\nYou won in {get_num_moves(target_grid)} move(s)!')


def play_versus_computer() -> None:
    """A two player game with computer opponent.

    (Examples not included since function depends on input and output.)
    """

    # Read the game file
    ship_symbols, ship_sizes, fleet_grid_player = read_game_file()
    # Make sure the game is valid
    if not is_valid_game(fleet_grid_player, ship_symbols, ship_sizes):
        print('The supplied game is not valid.  Game exiting.')
        return

    # Set up the game
    # Need target grid and fleet grid for both the human player and the
    # computer, and a flag to manage the taking of turns
    grid_size = len(fleet_grid_player)
    target_grid_player = get_target_grid(grid_size)
    hits_player = [0] * len(ship_sizes)

    fleet_grid_computer = generate_fleet_grid(grid_size, ship_symbols,
                                              ship_sizes)
    target_grid_computer = get_target_grid(grid_size)
    hits_computer = [0] * len(ship_sizes)

    player_turn = True

    # Play the game until it's over
    print('\n' + ':' * 10 + '  Human vs. Computer  ' + ':' * 10 + '\n')
    while not is_win(ship_sizes, hits_player) \
          and not is_win(ship_sizes, hits_computer):

        if player_turn:
            fleet_grid = fleet_grid_computer
            target_grid = target_grid_player
            display_grids(target_grid_player, fleet_grid_player)
            hits_list = hits_player
            need_to_find = []
            for i in range(len(ship_sizes)):
                need_to_find.append(ship_sizes[i] - hits_list[i])
            print('Your turn.')
            print(f'Ship sizes are {ship_sizes}.  ' \
                  f'You still need to find: {need_to_find}')
            [row, col] = get_valid_player_move(target_grid_player)
        else:
            fleet_grid = fleet_grid_player
            target_grid = target_grid_computer
            hits_list = hits_computer
            [row, col] = make_computer_guess(target_grid)
            print(f'Computer guess - row {row} and column {col}')

        print()

        result = make_move(row, col, fleet_grid, ship_symbols,
                           hits_list, target_grid)
        if player_turn:
            message = f'You {result}'
        else:
            message = f'Computer {result}'
        print(message)

        if is_not_given_symbol(row, col, fleet_grid, EMPTY):
            ship_index = ship_symbols.index(fleet_grid[row][col].lower())
            if hits_list[ship_index] >= ship_sizes[ship_index]:
                ship_size = ship_sizes[ship_index]
                ship_symbol = ship_symbols[ship_index]
                if player_turn:
                    print(f"The computer's size {ship_size} {ship_symbol} " \
                           "ship has been sunk!")
                else:
                    print(f"Your size {ship_size} {ship_symbol} " \
                           "ship has been sunk!")

        if player_turn:
            display_grids(target_grid_player, fleet_grid_player)
            if not is_win(ship_sizes, hits_list):
                input("\nPress enter so the Computer can take it's turn.\n")

        player_turn = not player_turn

    # Game is over, display results
    print()
    if is_win(ship_sizes, hits_player):
        print(f'You won in {get_num_moves(target_grid_player)} move(s)!')
    else:
        print(f'The computer won in {get_num_moves(target_grid_computer)}'
              + ' move(s).  Please try again.')


if __name__ == '__main__':
    # import doctest

    play_computer =True
    if play_computer:
        play_versus_computer()
    else:
        play_single_player()
