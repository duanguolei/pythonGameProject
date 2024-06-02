from a2_support import *


# Write your classes here
class Tile():
    def __init__(self):
        pass


    def is_blocking(self) -> bool:
        return False


    def get_type(self) -> str:
        return "Abstract Tile"


    def __str__(self):
        # self.get_type()
        return self.get_type()

    def __repr__(self):
        return self.get_type()

class Floor(Tile):

    def is_blocking(self) -> bool:
        return False

    def get_type(self) -> str:
        return FLOOR



class Wall(Tile):
    def is_blocking(self) -> bool:
        return True

    def get_type(self) -> str:
        return WALL



class Goal(Tile):
    def __init__(self):

        self.filled = False

    def is_blocking(self) -> bool:
        return False

    def get_type(self) -> str:
        return 'G'

    def is_filled(self) -> bool:
        return self.filled

    def fill(self) -> None:
        self.filled = True

    def __str__(self):
        return 'X' if self.filled else 'G'

    def __repr__(self):
        return 'X' if self.filled else 'G'

    def unfill(self):
        self.filled = False

class Entity:
    def __init__(self):
        pass

    def get_type(self) -> str:
        return "Abstract Entity"

    def is_movable(self) -> bool:
        return False

    def is_blocking(self) -> bool:
        return False

    def __str__(self) -> str:
        return self.get_type()

    def __repr__(self) -> str:
        return self.get_type()

class Crate(Entity):
    def __init__(self, strength: int):
        super().__init__()
        self.strength = strength

    def get_type(self) -> str:
        return 'C'

    def is_movable(self) -> bool:
        return True

    def get_strength(self) -> int:
        return self.strength

    def is_blocking(self) -> bool:
        return False

    def __str__(self):
        return str(self.strength)

    def __repr__(self):
        return str(self.strength)

class Potion(Entity):
    def __init__(self):
        super().__init__()

    def get_type(self) -> str:
        return 'Potion'

    def is_movable(self) -> bool:
        return False

    def effect(self) -> dict[str, int]:
        return {}




class StrengthPotion(Potion):
    def __init__(self):
        super().__init__()

    def get_type(self) -> str:
        return 'S'

    def effect(self) -> dict[str, int]:
        return {'strength': 2}

class MovePotion(Potion):
    def __init__(self):
        super().__init__()

    def get_type(self) -> str:
        return 'M'

    def effect(self) -> dict[str, int]:
        return {'moves': 5}

class FancyPotion(Potion):
    def __init__(self):
        super().__init__()

    def get_type(self) -> str:
        return 'F'

    def effect(self) -> dict[str, int]:
        return {'strength': 2, 'moves': 2}

class Player(Entity):
    def __init__(self, start_strength: int, moves_remaining: int):
        super().__init__()
        self.strength = start_strength
        self.moves_remaining = moves_remaining

    def get_type(self) -> str:
        return PLAYER

    def get_strength(self) -> int:
        return self.strength

    def add_strength(self, amount: int) -> None:
        self.strength += amount

    def get_moves_remaining(self) -> int:
        return self.moves_remaining

    def add_moves_remaining(self, amount: int) -> None:
        self.moves_remaining += amount

    def apply_effect(self, potion_effect: dict[str, int]) -> None:
        if 'strength' in potion_effect:
            self.add_strength(potion_effect['strength'])
        if 'moves' in potion_effect:
            self.add_moves_remaining(potion_effect['moves'])

    def is_movable(self) -> bool:
        return True


def convert_maze(game: list[list[str]]) -> tuple[Grid, Entities, Potion]:
        grid = []
        entities = {}
        player_position = None

        for row_index, row in enumerate(game):
            grid_row = []
            for col_index, cell in enumerate(row):

                try:

                    cell=int(cell)
                    crate=Crate(cell)
                    entities[(row_index, col_index)] = crate  # You may adjust the strength as needed
                    grid_row.append(Floor())

                except:
                    if cell == 'P':
                        player_position = (row_index, col_index)
                        grid_row.append(Floor())

                    elif cell == 'S':
                        strengthPotion=StrengthPotion()
                        entities[(row_index, col_index)] = strengthPotion
                        grid_row.append(Floor())

                    elif cell == 'M':
                        movePotion=MovePotion()
                        grid_row.append(Floor())
                        entities[(row_index, col_index)] = movePotion

                    elif cell == 'F':
                        fancyPotion=FancyPotion()
                        grid_row.append(Floor())
                        entities[(row_index, col_index)] = fancyPotion

                    elif cell == 'G':
                        gobal=Goal()
                        grid_row.append(gobal)

                    elif cell == 'W':
                        grid_row.append(Wall())

                    else:
                        grid_row.append(Floor())


            grid.append(grid_row)

        return (grid, entities, player_position)


class SokobanModel:
    def __init__(self, maze_file: str) -> None:
        raw_maze, player_stats = read_file(maze_file)

        self.player_strength, self.player_moves_remaining = player_stats
        self.maze, self.entities, self.player_position =convert_maze(raw_maze)

        self.undo_goal_postion=(0,0)

    def get_maze(self) ->Grid:
        return self.maze

    def get_entities(self) -> Entities:
        return self.entities

    def get_player_position(self) -> tuple[int, int]:
        return self.player_position

    def get_player_moves_remaining(self) -> int:
        return self.player_moves_remaining

    def get_player_strength(self) -> int:
        return self.player_strength

    def undo(self)->None:
        self.player_strength = self.copy_player_strength
        self.player_moves_remaining = self.copy_player_moves_remaining
        self.player_position = self.copy_player_postions
        self.entities = self.copy_entities
        self.maze = self.copy_maze
        if isinstance(self.maze[self.undo_goal_postion[0]][self.undo_goal_postion[1]],Goal):
            self.maze[self.undo_goal_postion[0]][self.undo_goal_postion[1]].unfill()


    def attempt_move(self, direction: str) -> bool:
        if not self.is_valid_move(direction):
            return False

        self.copy_player_strength = int(self.get_player_strength())
        self.copy_player_moves_remaining = int(self.get_player_moves_remaining())
        self.copy_player_postions =tuple(self.player_position)
        self.copy_entities = dict(self.get_entities())
        self.copy_maze = list(self.get_maze())

        row, col = self.player_position
        # print(DIRECTION_DELTAS)
        delta_row, delta_col = DIRECTION_DELTAS[direction]
        new_row, new_col = row + delta_row, col + delta_col
        new_position = (new_row, new_col)



        if self.is_valid_position(new_position):
            entity = self.entities.get(new_position)

            if entity is None:
                self.move_player(new_position)
                return True
            else:

                flage=self.move_crate(new_position,entity,direction)
                return flage
        else:
            return False

    def move_player(self, new_position: Position) -> None:

        if not isinstance(self.maze[self.player_position[0]][self.player_position[1]],Goal):
            self.maze[self.player_position[0]][self.player_position[1]] = Floor()


        self.player_position = new_position
        self.player_moves_remaining -= 1

    def move_crate(self, crate_position: Position, empty:Entity,direction:str) ->bool:
        new_row, new_cow = crate_position[0], crate_position[1]
        delta_row, delta_col = DIRECTION_DELTAS[direction]

        next_row, next_cow = new_row + delta_row, new_cow + delta_col
        self.undo_goal_postion = (next_row, next_cow)

        if empty.get_type()=="C":
            if empty.get_strength()<=self.player_strength:

                if self.maze[next_row][next_cow]==FLOOR or isinstance(self.maze[next_row][next_cow],Floor):
                    self.entities.pop(crate_position)
                    self.entities[(next_row,next_cow)]=empty
                    self.move_player(crate_position)
                    return True


                elif isinstance(self.maze[next_row][next_cow],Goal):
                    next_empty=self.maze[next_row][next_cow]
                    next_empty.fill()

                    self.entities.pop(crate_position)
                    self.move_player(crate_position)
                    return True

                elif isinstance(self.maze[next_row][next_cow],Wall):
                    return False

                else:
                    next_empty=self.entities[(next_row,next_cow)]
                    player = Player(self.get_player_strength(), self.get_player_moves_remaining())
                    player.apply_effect(next_empty.effect)
                    self.entities.pop(crate_position)
                    self.entities[(next_row,next_cow)]=empty
                    self.player_strength = player.get_strength()
                    self.player_moves_remaining = player.get_moves_remaining()
                    self.move_player(crate_position)

                    return True

            else:
                return False

        else:
            player=Player(self.get_player_strength(),self.get_player_moves_remaining())
            empty_effect=empty.effect()
            player.apply_effect(empty_effect)
            self.player_strength=player.get_strength()
            self.player_moves_remaining=player.get_moves_remaining()
            self.entities.pop(crate_position)
            self.move_player(crate_position)
            return True

    def is_valid_move(self, move: str) -> bool:
        return move in DIRECTION_DELTAS.keys()

    def is_valid_position(self, position: Position) -> bool:

        row, col = position
        tile=self.maze[row][col]
        if isinstance(tile,Tile):
            if tile.is_blocking():
                return False
            else:
                return True

        else:
            return True


    def has_won(self) -> bool:
        for position, entity in self.entities.items():
            if isinstance(entity, Crate):
                return False
        return True

    def has_lost(self) -> bool:
        if self.get_player_moves_remaining()<=0:
            return True
        else:
            return False




class Sokoban:
    def __init__(self, maze_file: str) -> None:
        self.model = SokobanModel(maze_file)
        self.view = SokobanView()

    def display(self) -> None:


        self.view.display_game(self.model.get_maze(),self.model.get_entities(),
                               self.model.get_player_position())

        self.view.display_stats(self.model.get_player_moves_remaining(),
                                self.model.get_player_strength())

    def play_game(self) -> None:
        while True:
            self.display()
            move = input("Enter move: ").strip()

            if move == 'q':
                break
            elif move == 'u':

                self.model.undo()

            elif self.model.attempt_move(move):
                if self.model.has_won():
                    break
                elif self.model.has_lost():
                    break
                else:
                    continue
            else:
                print('Invalid move\n')

        self.show_result()

    def show_result(self)->None:


        if self.model.has_won():
            self.display()
            print('You won!')
        elif self.model.has_lost():
            print('You lost!')




def main():
    maze_file = 'maze_files/maze3.txt'
    game = Sokoban(maze_file)
    game.play_game()




if __name__ == '__main__':
    main()
