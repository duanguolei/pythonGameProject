import tkinter as tk
from PIL import ImageTk, Image
from typing import Union


MAZE_SIZE = 450
SHOP_WIDTH = 200
BANNER_HEIGHT = 75
STATS_HEIGHT = 75
FONT = ('Arial', 16, 'bold')
TITLE_FONT = ('Arial', 18, 'bold')
CRATE_FONT = ('Arial', 20, 'bold')


def get_image(
    image_name: str,
    size: tuple[int, int],
    cache: dict[str, ImageTk.PhotoImage] = None
) -> ImageTk.PhotoImage:
    """ Returns the cached image for image_id if one exists, otherwise creates a
        new one, caches and returns it.

    Parameters:
        image_name: The path to the image to load.
        size: The size to resize the image to, as (width, height).
        cache: The cache to use. If None, no caching is performed.

    Returns:
        The image for the given image_name, resized appropriately.
    """
    if cache is None or image_name not in cache:
        image = ImageTk.PhotoImage(image=Image.open(image_name).resize(size))
        if cache is not None:
            cache[image_name] = image
    elif image_name in cache:
        return cache[image_name]
    return image


class AbstractGrid(tk.Canvas):
    """ A type of tkinter Canvas that provides support for using the canvas as a
        grid (i.e. a collection of rows and columns). """

    def __init__(
        self,
        master: Union[tk.Tk, tk.Frame],
        dimensions: tuple[int, int],
        size: tuple[int, int],
        **kwargs
    ) -> None:
        """ Constructor for AbstractGrid.

        Parameters:
            master: The master frame for this Canvas.
            dimensions: (#rows, #columns)
            size: (width in pixels, height in pixels)
        """
        super().__init__(
            master,
            width=size[0] + 1,
            height=size[1] + 1,
            highlightthickness=0,
            **kwargs
        )
        self._size = size
        self.set_dimensions(dimensions)

    def set_dimensions(self, dimensions: tuple[int, int]) -> None:
        """ Sets the dimensions of the grid.

        Parameters:
            dimensions: Dimensions of this grid as (#rows, #columns)
        """
        self._dimensions = dimensions

    def get_cell_size(self) -> tuple[int, int]:
        """ Returns the size of the cells (width, height) in pixels. """
        rows, cols = self._dimensions
        width, height = self._size
        return width // cols, height // rows

    def pixel_to_cell(self, x: int, y: int) -> tuple[int, int]:
        """ Converts a pixel position to a cell position.

        Parameters:
            x: The x pixel position.
            y: The y pixel position.

        Returns:
            The (row, col) cell position.
        """
        cell_width, cell_height = self.get_cell_size()
        return y // cell_height, x // cell_width

    def get_bbox(self, position: tuple[int, int]) -> tuple[int, int, int, int]:
        """ Returns the bounding box of the given (row, col) position.

        Parameters:
            position: The (row, col) cell position.

        Returns:
            Bounding box for this position as (x_min, y_min, x_max, y_max).
        """
        row, col = position
        cell_width, cell_height = self.get_cell_size()
        x_min, y_min = col * cell_width, row * cell_height
        x_max, y_max = x_min + cell_width, y_min + cell_height
        return x_min, y_min, x_max, y_max

    def get_midpoint(self, position: tuple[int, int]) -> tuple[int, int]:
        """ Gets the graphics coordinates for the center of the cell at the
            given (row, col) position.

        Parameters:
            position: The (row, col) cell position.

        Returns:
            The x, y pixel position of the center of the cell.
        """
        row, col = position
        cell_width, cell_height = self.get_cell_size()
        x_pos = col * cell_width + cell_width // 2
        y_pos = row * cell_height + cell_height // 2
        return x_pos, y_pos

    def annotate_position(
        self,
        position: tuple[int, int],
        text: str,
        font=None
    ) -> None:
        """ Annotates the cell at the given (row, col) position with the
            provided text.

        Parameters:
            position: The (row, col) cell position.
            text: The text to draw.
        """
        self.create_text(self.get_midpoint(position), text=text, font=font)

    def clear(self):
        """ Clears all child widgets off the canvas. """
        self.delete("all")
