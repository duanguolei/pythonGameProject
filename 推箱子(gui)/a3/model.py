from a2_support import *

COIN = '$'
COIN_AMOUNT = 5


class Tile:
    """ Abstract class for a tile in the maze. """
    TYPE = 'Abstract Tile'
    BLOCKING = False

    def is_blocking(self) -> bool:
        """ Returns True iff this tile is blocking. """
        return self.BLOCKING

    def get_type(self) -> str:
        """ Returns the type of this tile. """
        return self.TYPE

    def __str__(self) -> str:
        return self.get_type()

    def __repr__(self) -> str:
        return str(self)


class Floor(Tile):
    """ A basic floor tile (non-blocking) in the maze. """
    TYPE = FLOOR


class Wall(Tile):
    """ A basic wall tile (blocking) in the maze. """
    TYPE = WALL
    BLOCKING = True


class Goal(Tile):
    """ A goal tile onto which crates should be pushed in the maze. """
    TYPE = GOAL

    def __init__(self) -> None:
        """ Constructor for Goal. Goal is initially unfilled. """
        super().__init__()
        self._is_filled = False

    def fill(self) -> None:
        """ Fills this goal. """
        self._is_filled = True

    def unfill(self) -> None:
        """ Unfills this goal. """
        self._is_filled = False

    def is_filled(self) -> bool:
        """ Returns True iff the goal is filled. """
        return self._is_filled

    def __str__(self):
        return FILLED_GOAL if self._is_filled else self.get_type()


class Entity:
    """ Abstract class for an entity in the maze. """
    TYPE = 'Abstract Entity'
    MOVABLE = False

    def get_type(self) -> str:
        """ Returns the type of this entity. """
        return self.TYPE

    def is_movable(self) -> bool:
        """ Returns True iff this entity is movable. """
        return self.MOVABLE

    def __str__(self):
        return self.get_type()

    def __repr__(self):
        return str(self)


class Crate(Entity):
    """ A crate entity in the maze. """
    TYPE = CRATE
    MOVABLE = True

    def __init__(self, strength: int) -> None:
        """ Constructor for Crate.

        Parameters:
            strength: The strength required to push this crate.
        """
        super().__init__()
        self._strength = strength

    def get_strength(self) -> int:
        """ Returns the strength required to push this crate. """
        return self._strength

    def __str__(self):
        return str(self._strength)


class Coin(Entity):
    """ A coin entity in the maze, which can be collected by a player to
        increase their money.
    """
    TYPE = COIN


class Potion(Entity):
    """ Abstract class for a potion entity in the maze. """
    TYPE = 'Potion'
    EFFECT = {}

    def effect(self) -> dict[str, int]:
        """ Returns the effect of this potion. Keys that may (or may not) exist
            in this dictionary are 'strength' and 'moves'.
        """
        return self.EFFECT


class StrengthPotion(Potion):
    """ A potion that increases the strength of the player. """
    TYPE = STRENGTH_POTION
    EFFECT = {'strength': 2}


class MovePotion(Potion):
    """ A potion that increases the moves remaining for the player. """
    TYPE = MOVE_POTION
    EFFECT = {'moves': 5}


class FancyPotion(Potion):
    """ A potion that increases both the strength and moves remaining for the
        player.
    """
    TYPE = FANCY_POTION
    EFFECT = {'strength': 2, 'moves': 2}


class Player(Entity):
    """ A player entity in the maze. """
    TYPE = PLAYER

    def __init__(self, start_strength: int, moves_remaining: int) -> None:
        """ Constructor for Player.

        Parameters:
            start_strength: The starting strength of the player.
            moves_remaining: The number of moves the player can make.
        """
        super().__init__()
        self._strength = start_strength
        self._moves_remaining = moves_remaining
        self._money = 0

    def get_money(self) -> int:
        """ Returns the amount of money the player has. """
        return self._money

    def add_money(self, money: int) -> None:
        """ Adds money to the player's total.

        Parameters:
            money: The amount of money to add. This may be positive or negative.
        """
        self._money += money

    def is_movable(self) -> bool:
        """ Returns True iff the player is movable. """
        return self._moves_remaining > 0

    def get_strength(self) -> int:
        """ Returns the strength of the player. """
        return self._strength

    def add_strength(self, strength: int) -> None:
        """ Adds strength to the player.

        Parameters:
            strength: The amount of strength to add.
        """
        self._strength += strength

    def get_moves_remaining(self) -> int:
        """ Returns the number of moves remaining for the player. """
        return self._moves_remaining

    def add_moves_remaining(self, moves: int) -> None:
        """ Adds moves to the player's moves remaining.

        Parameters:
            moves: The number of moves to add. This may be positive or negative.
        """
        self._moves_remaining += moves

    def apply_effect(self, potion_effect: dict[str, int]) -> None:
        """ Applies the effects described in potion_effect to the player.

        Parameters:
            potion_effect: The effect of the potion. Only the keys 'strength'
                            and 'moves' will be considered.
        """
        self.add_strength(potion_effect.get('strength', 0))
        self.add_moves_remaining(potion_effect.get('moves', 0))


TILE_IDS_TO_CLASS = {
    FLOOR: Floor,
    WALL: Wall,
    GOAL: Goal,
    FILLED_GOAL: Goal,
}

ENTITY_IDS_TO_CLASS = {
    CRATE: Crate,
    COIN: Coin,
    PLAYER: Player,
    STRENGTH_POTION: StrengthPotion,
    MOVE_POTION: MovePotion,
    FANCY_POTION: FancyPotion,
}


def convert_maze(raw_maze: list[list[str]]) -> tuple[Grid, Entities, Position]:
    """ Converts a raw maze into a proper maze, entities and player position.

    Parameters:
        raw_maze: The raw maze from the file.

    Returns:
        A tuple containing three items:
            1) The maze as a list of lists (rows) of tile objects.
            2) A dictionary mapping (row, col) positions to the entities at
                those positions on the maze. Positions only exist in this
                dictionary if there is an entity at that position.
            3) The player's starting position.
    """
    proper_maze = []
    entities = {}
    player_position = None

    for i, row in enumerate(raw_maze):
        new_row = []
        for j, tile_type in enumerate(row):
            tile = TILE_IDS_TO_CLASS.get(tile_type, Floor)()
            if tile_type == FILLED_GOAL:
                tile.fill()

            new_row.append(tile)
            if not TILE_IDS_TO_CLASS.get(tile_type):
                if tile_type == PLAYER:
                    player_position = (i, j)
                else:
                    if tile_type.isdigit():
                        tile_type = int(tile_type)
                        entity = Crate(tile_type)
                    else:
                        entity = ENTITY_IDS_TO_CLASS.get(tile_type)()

                    entities[(i, j)] = entity
        proper_maze.append(new_row)
    return proper_maze, entities, player_position


class SokobanModel:
    """ A model for a Sokoban game. """
    ITEM_COSTS = {
        STRENGTH_POTION: 5,
        MOVE_POTION: 5,
        FANCY_POTION: 10,
    }

    def __init__(self, maze_file: str) -> None:
        """ Constructor for SokobanModel.

        Parameters:
            maze_file: The path to the maze file (e.g. 'maze_files/maze1.txt')
        """
        self._maze_file = maze_file
        self.reset()

    def reset(self) -> None:
        """ Resets the model to its initial state. """
        raw_maze, player_stats = read_file(self._maze_file)
        self._maze, self._entities, self._player_position = convert_maze(
            raw_maze)
        self._player = Player(*player_stats)

        self._last_state = {
            'maze': [[item for item in row] for row in self._maze],
            'entities': {key: value for key, value in self._entities.items()},
            'player_stats': player_stats,
            'player_position': self._player_position,
            'last_filled': None,
        }

    def get_shop_items(self) -> dict[str, int]:
        """ Returns a dictionary mapping item names to their cost. """
        return self.ITEM_COSTS

    def attempt_purchase(self, item: str) -> bool:
        """ Attempts to purchase the given item.

        Parameters:
            item: The id / type of the item to purchase.
        """
        if self._player.get_money() < self.ITEM_COSTS.get(item):
            return False

        self._player.add_money(-self.ITEM_COSTS[item])
        self._entities[self._player_position] = ENTITY_IDS_TO_CLASS[item]()
        self._handle_potion(self._player_position)
        return True

    def get_maze(self) -> Grid:
        """ Returns the maze. """
        return self._maze

    def get_dimensions(self) -> tuple[int, int]:
        """ Returns the dimensions of the maze as (#rows, #columns). """
        return len(self._maze), len(self._maze[0])

    def get_entities(self) -> Entities:
        """ Returns a dictionary mapping (row, col) positions to the entities at
            those positions on the maze. Positions only exist in this dictionary
            if there is an entity at that position.
        """
        return self._entities

    def get_player_position(self) -> Position:
        """ Returns the player's current position. """
        return self._player_position

    def get_player_moves_remaining(self) -> int:
        """ Returns the number of moves remaining for the player. """
        return self._player.get_moves_remaining()

    def get_player_strength(self) -> int:
        """ Returns the player's current strength. """
        return self._player.get_strength()

    def get_player_money(self) -> int:
        """ Returns the amount of money the player has. """
        return self._player.get_money()

    def undo_move(self) -> None:
        """ Undoes the last valid move made by the player. """
        self._maze = self._last_state['maze']
        self._entities = self._last_state['entities']
        self._player_position = self._last_state['player_position']
        self._player = Player(*self._last_state['player_stats'])
        if self._last_state['last_filled'] is not None:
            row, col = self._last_state['last_filled']
            self._get_tile(row, col).unfill()

    def attempt_move(self, direction: str) -> bool:
        """ Attempts to move the player in the given direction.

        Parameters:
            direction: The direction to move in. This should be one of the
                        constants UP, DOWN, LEFT or RIGHT, or 'u' for undo.

        Returns:
            True iff the move was successful.
        """
        # Handle undo move
        if direction == 'u':
            self.undo_move()
            return True

        # Make a copy of important information about this state to overwrite
        # self._last_state if the move is successful
        last_state = {
            'maze': [[item for item in row] for row in self._maze],
            'entities': {key: value for key, value in self._entities.items()},
            'player_stats': (self._player.get_strength(),
                             self._player.get_moves_remaining()),
            'player_position': self._player_position,
            'last_filled': None,
        }

        # Handle directional move
        if not DIRECTION_DELTAS.get(direction):
            return False

        new_position = new_row, new_col = self._get_new_position(
            self._player_position, direction)

        if not self._in_bounds(new_row, new_col):
            return False

        if self._get_tile(new_row, new_col).is_blocking():
            return False

        # Handle case where there is a crate in the new position
        entity_present = self._entities.get(new_position)
        if entity_present is not None:
            if entity_present.get_type() == CRATE:
                if not self._attempt_push(new_position, direction):
                    return False
            elif entity_present.get_type() == COIN:
                self._player.add_money(COIN_AMOUNT)
                self._entities.pop(new_position)

            elif isinstance(entity_present, Potion):
                self._handle_potion(new_position)

        self._player_position = new_position
        self._player.add_moves_remaining(-1)

        self._last_state = last_state
        return True

    def has_won(self) -> bool:
        """ Returns True iff the player has won the game. """
        for row in self._maze:
            for tile in row:
                if tile.get_type() == GOAL and not tile.is_filled():
                    return False
        return True

    def _get_new_position(self, position: Position, direction: str) -> Position:
        """ Returns the new position for an entity if it were to move in the
            given direction from the given position. This does not consider
            whether the move is valid.

        Parameters:
            position: The current (row, column) position.
            direction: The direction in which to move. This should be one of the
                        constants UP, DOWN, LEFT or RIGHT.

        Returns:
            The new (row, column) position for the entity.
        """
        delta = DIRECTION_DELTAS.get(direction)
        return position[0] + delta[0], position[1] + delta[1]

    def _get_tile(self, row: int, col: int) -> Tile:
        """ Returns the tile at the given (row, col) position.

        Parameters:
            row: The row of the tile.
            col: The column of the tile.

        Returns:
            The tile at the given position.

        Preconditions:
            The given position is in bounds for the maze.
        """
        return self._maze[row][col]

    def _in_bounds(self, row: int, col: int) -> bool:
        """ Returns True iff the given (row, col) position is in bounds for the
            maze.

        Parameters:
            row: The row of the position.
            col: The column of the position.

        Returns:
            True iff the given position is in bounds for the maze.
        """
        return 0 <= row < len(self._maze) and 0 <= col < len(self._maze[0])

    def _attempt_push(self, position: Position, direction: str) -> bool:
        """ Attempts to push a crate from the given position in the given
            direction.

        Parameters:
            position: The current (row, col) position of the crate.
            direction: The direction in which to push the crate. This should be
                        one of the constants UP, DOWN, LEFT or RIGHT.

        Returns:
            True iff the crate was successfully pushed.
        """
        new_row, new_col = self._get_new_position(position, direction)
        tile = self._get_tile(new_row, new_col)

        # If the new position is out of bounds, or contains a blocking tile or
        # entity, return False
        if not self._in_bounds(new_row, new_col):
            return False
        if tile.is_blocking():
            return False
        if (new_row, new_col) in self._entities:
            return False

        # If the player isn't strong enough for this crate, return False
        crate_strength = self._entities.get(position).get_strength()
        if crate_strength > self._player.get_strength():
            return False

        crate = self._entities.pop(position)

        # If the crate would fill an unfilled goal, do so and don't add the
        # crate back to the entities
        if tile.get_type() == GOAL and not tile.is_filled():
            tile.fill()
            self._last_state['last_filled'] = (new_row, new_col)
            return True

        # Otherwise, add the crate back to the entities
        self._entities[(new_row, new_col)] = crate
        return True

    def _handle_potion(self, position: tuple[int, int]) -> None:
        """ Handles applying the effect of a potion at the given position to the
            player.

        Parameters:
            position: The position of the potion.
        """
        potion = self._entities.pop(position)
        self._player.apply_effect(potion.effect())
