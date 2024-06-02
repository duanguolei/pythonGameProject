NAUGHT = "O"
CROSS = "X"
EMPTY = "  "

# PIECES_PER_PLAYER is not guaranteed to stay at 9 in all tests, but is
# guaranteed to be an integer in the range [5, 9].
PIECES_PER_PLAYER = 5

# GRID_SIZE is guaranteed to remain as 3 for all CSSE1001 tests. For CSSE7030
# tests, GRID_SIZE may change to be in the range [2, 8]
GRID_SIZE = 3

HELP_MESSAGE = 'Enter a row, column & piece size in the format: row col size\n'
INVALID_FORMAT_MESSAGE = 'Invalid move format. Please try again.\n'
INVALID_ROW_MESSAGE = 'Invalid row. Please try again.\n'
INVALID_COLUMN_MESSAGE = 'Invalid column. Please try again.\n'
INVALID_SIZE_MESSAGE = 'Invalid piece size. Please try again.\n'
INVALID_MOVE_MESSAGE = 'Invalid move. Ensure you have a piece of the requested size, and that you\'re not putting it over a bigger piece and try again!'
