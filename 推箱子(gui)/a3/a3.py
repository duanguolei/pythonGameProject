
from tkinter import messagebox, filedialog
from typing import Callable
from model import SokobanModel, Tile, Entity
from a2_support import *
from a3_support import *

# Write your classes and functions here

class FancyGameView(AbstractGrid):
    def __init__(
        self,
        master: tk.Frame | tk.Tk,
        dimensions: tuple[int, int],
        size: tuple[int, int],
        **kwargs
    ) -> None:
        """
        Initialize the FancyGameView.

        :param master: The tkinter widget.
        :param dimensions: The dimensions of the grid.
        :param size: The size of grid.
        :param kwargs: Additional options.
        """
        super().__init__(
            master,
            dimensions,
            size
        )

        self._image_cache = {}

    def display(
        self,
        maze: Grid,
        entities: Entities,
        player_position: Position
    ):
        """
        Display the maze, entities, and player on the grid.

        :param maze: The maze grid.
        :param entities: The entities on the grid.
        :param player_position: The position of the player.
        """
        self.clear()
        cell_width, cell_height = self.get_cell_size()

        for row, line in enumerate(maze):
            for col, tile in enumerate(line):
                type_ = maze[row][col]
                str_type_ = type_.get_type()

                if str_type_ == FLOOR:
                    image_name = 'images/Floor.png'
                elif str_type_ == WALL:
                    image_name = 'images/W.png'
                elif str_type_ == GOAL:
                    if type_.is_filled():
                        image_name = 'images/X.png'
                    else:
                        image_name = 'images/G.png'

                image = get_image(image_name, (cell_width, cell_height), self._image_cache)
                x, y = self.get_midpoint((row, col))
                self._image_cache[image_name] = image
                self.create_image(x, y, image=image)
        #
        for position, entity in entities.items():
            str_type_ = entity.get_type()

            if str_type_ == CRATE:
                image_name = 'images/C.png'
            elif str_type_ == FANCY_POTION:
                image_name = 'images/F.png'
            elif str_type_ == MOVE_POTION:
                image_name = 'images/M.png'
            elif str_type_ == STRENGTH_POTION:
                image_name = 'images/S.png'
            elif str_type_ == "$":
                image_name = 'images/$.png'

            image = get_image(image_name, (cell_width, cell_height), self._image_cache)
            x, y = self.get_midpoint(position)
            self.create_image(x, y, image=image)
            self._image_cache[image_name] = image

            if str_type_ == CRATE:
                strength = entity.get_strength()
                self.annotate_position((position[0], position[1]), text=str(strength), font=CRATE_FONT)

        player_image_name = 'images/P.png'
        player_image = get_image(player_image_name, (cell_width, cell_height), self._image_cache)
        self._image_cache[player_image_name] = player_image
        x, y = self.get_midpoint(player_position)
        self.create_image(x, y, image=player_image)


class FancyStatsView(AbstractGrid):
    def __init__(self, master: tk.Tk or tk.Frame) -> None:
        """
        Initialize the FancyStatsView.

        :param master: The tkinter widget.
        """
        super().__init__(master, (3, 3), (660, STATS_HEIGHT))

    def draw_stats(self, moves_remaining: int, strength: int, money: int) -> None:
        """
        Draw the player statistics.

        :param moves_remaining: Remaining moves for the player.
        :param strength: Strength of the player.
        :param money: Player's money.
        """
        self.clear()

        self.annotate_position((0, 1), text="Player Stats", font=('Arial', 18, 'bold'))

        self.annotate_position((1, 0), text="Moves remaining:")
        self.annotate_position((1, 1), text="Strength:")
        self.annotate_position((1, 2), text="Money:")

        self.annotate_position((2, 0), text=str(moves_remaining))
        self.annotate_position((2, 1), text=str(strength))
        self.annotate_position((2, 2), text="$" + str(money))


class Shop(tk.Frame):
    def __init__(self, master: tk.Frame) -> None:
        """
        Initialize the Shop.

        :param master: The tkinter widget.
        """
        super().__init__(master,)

        self.config(width=SHOP_WIDTH, height=MAZE_SIZE)

        self.title_label = tk.Label(self, text="Shop", font=FONT)
        self.title_label.pack(side=tk.TOP)

    def create_buyable_item(self, item: str, amount: int, callback: Callable[[], None]
    ) -> None:
        """
        Create a buyable item in the shop.

        :param item: The item identifier.
        :param amount: The cost of the item.
        :param callback: The callback function when the item is bought.
        """
        if item.upper() == "S":
            good = 'Strength Potion'
        elif item.upper() == "M":
            good = 'Move Potion'
        elif item.upper() == 'F':
            good = 'Fancy Potion'

        label_text = f"{good}: ${amount}"

        frame = tk.Frame(self, width=SHOP_WIDTH, height=30,bg='red')
        frame.pack()
        frame.pack_propagate(False)
        item_label = tk.Label(frame, text=label_text, width=20, height=30)
        item_label.pack(side=tk.LEFT)

        buy_button = tk.Button(frame, text="Buy", command=lambda: callback(item), width=7, height=20, bg='white')
        buy_button.pack(side=tk.RIGHT)


# FancySokobanView class
class FancySokobanView:
    def __init__(self, master: tk.Tk, dimensions: tuple[int, int], size: tuple[int, int]) -> None:
        """
        Initialize the FancySokobanView,and initialize the entire game interface and layout

        :param master: The tkinter widget.
        :param dimensions: The dimensions of the grid.
        :param size: The size of grid.
        """
        global banner_image
        banner_image = get_image('images/banner.png', size=(660, BANNER_HEIGHT))
        title_banner = tk.Label(master, image=banner_image)
        title_banner.pack()

        self.frame_2 = tk.Frame(master, width=660, height=MAZE_SIZE)
        self.frame_2.pack()
        self.frame_3 = tk.Frame(master, width=660, height=STATS_HEIGHT)
        self.frame_3.pack()

        self.F_G_view = FancyGameView(self.frame_2, dimensions=dimensions, size=(MAZE_SIZE, MAZE_SIZE))
        self.F_G_view.pack(side=tk.LEFT)

        self.shop = Shop(self.frame_2)
        self.shop.pack_propagate(0)
        self.shop.pack(side=tk.RIGHT)

        self.F_S_view = FancyStatsView(self.frame_3)
        self.F_S_view.pack(side=tk.BOTTOM)

    def display_game(self, maze: Grid, entities: Entities, player_position: Position) -> None:
        """
        Display the game grid.

        :param maze: The maze grid.
        :param entities: The entities on the grid.
        :param player_position: The position of the player.
        """
        self.F_G_view.clear()
        self.F_G_view.display(maze, entities, player_position)

    def display_stats(self, moves: int, strength: int, money: int) -> None:
        """
        Display player statistics.

        :param moves: Remaining moves for the player.
        :param strength: Strength of the player.
        :param money: Player's money.
        """
        self.F_S_view.clear()
        self.F_S_view.draw_stats(moves, strength, money)

    def create_shop_items(self, shop_items: dict[str, int], button_callback: Callable[[str], None] | None = None) -> None:
        """
        Create items in the shop.

        :param shop_items: A dictionary of shop items and their prices.
        :param button_callback: The callback function when an item is bought.
        """
        print(shop_items.items())
        for key, value in shop_items.items():
            self.shop.create_buyable_item(key, value, button_callback)


class ExtraFancySokoban:
    def __init__(self, root: tk.Tk, maze_file: str) -> None:
        """
        Initialize the ExtraFancySokoban.

        :param root: The root Tkinter .
        :param maze_file: The file containing the maze.
        """
        self.root = root
        self.model = SokobanModel(maze_file=maze_file)
        self.SokobanView = FancySokobanView(self.root, self.model.get_dimensions(), size=(MAZE_SIZE, MAZE_SIZE))

        self.redraw()

        self.SokobanView.create_shop_items(self.model.get_shop_items(), self.create_shop_event)

        self.create_menu()

        self.root.bind('<KeyPress>', self.handle_keypress)

    def create_menu(self):
        """
        Create the menu for the application.
        """
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.menuFile = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='File', menu=self.menuFile)
        self.menuFile.add_command(label='Save', command=self.save_file)
        self.menuFile.add_command(label='Load', command=self.load_file)

    def save_file(self):
        """
        Save the current game state to a file.
        """
        filename = filedialog.asksaveasfilename()
        entities = self.model.get_entities()
        strength = self.model.get_player_strength()
        moves_remaining = self.model.get_player_moves_remaining()
        player_position = self.model.get_player_position()
        maze = self.model.get_maze()

        new_maze = []

        for m in maze:
            new_maze.append([i.get_type() for i in m])

        for key, value in entities.items():
            if value.get_type() == CRATE:
                new_maze[key[0]][key[1]] = str(value.get_strength())
            else:
                new_maze[key[0]][key[1]] = value.get_type()

        new_maze[player_position[0]][player_position[1]] = "P"

        with open(filename + '.txt', 'w', encoding='utf-8') as f:
            f.write(f"{strength} {moves_remaining}\n")
            for m in new_maze:
                f.write(''.join(m))
                f.write('\n')

    def load_file(self) -> None:
        """
        Load a game state from a file.
        """
        file = filedialog.askopenfilename()
        self.model = SokobanModel(maze_file=file)
        self.redraw()

    def redraw(self):
        """
        Redraw the game view.
        """
        self.SokobanView.display_game(maze=self.model.get_maze(), entities=self.model.get_entities(),
                                      player_position=self.model.get_player_position())
        self.SokobanView.display_stats(self.model.get_player_moves_remaining(), self.model.get_player_strength(),
                                       self.model.get_player_money())

    def continue_game(self, flag):
        """
        Continue or end the game based on the flag.

        :param flag: The flag indicating win or loss.
        """
        result = messagebox.askyesno('', message=f'You {flag}! Play again?')
        if result:
            self.model.reset()
            self.redraw()
        else:
            self.root.destroy()

    def handle_keypress(self, event: tk.Event) -> None:
        """
        Handle key presses during the game.

        :param event: The key press event.
        """
        char = event.char.lower()
        if char in [UP, DOWN, LEFT, RIGHT]:
            self.model.attempt_move(char)
            self.redraw()
            if self.model.has_won():
                self.continue_game('won')
            elif self.model.get_player_moves_remaining() == 0:
                self.continue_game('lost')
        elif char == 'u':
            self.model.undo_move()
            self.redraw()
        else:
            pass

    def create_shop_event(self, item_id: str):
        """
        Handle the event of buying an item from the shop.

        :param item_id: The identifier of the item.
        """
        self.model.attempt_purchase(item_id)
        self.redraw()


def play_game(root: tk.Tk, maze_file: str) -> None:
    """
    Start playing the game.

    :param root: The root Tkinter widget.
    :param maze_file: The file containing the maze.
    """
    root.title(string="Extra Fancy Sokoban")
    ExtraFancySokoban(root, maze_file)
    root.mainloop()


def main() -> None:
    """ The main function. """
    root = tk.Tk()

    width = 660
    height = 600

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(False, False)

    file = './maze_files/coin_maze.txt'

    play_game(root, file)


if __name__ == "__main__":
    main()
