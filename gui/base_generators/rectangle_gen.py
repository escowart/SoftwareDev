from gui.base_generators.basic_gen import *


class RectangleIGen(BasicIGen):
    """ A class representing a Rectangle Image Generator
    """
    def __init__(self,
                 width: Natural,
                 height: Natural,
                 **kwargs: dict) -> None:
        """ Construct a rectangle
        :param width: The width of the rectangle
        :param height: The height of the rectangle
        :param kwargs: The keyword arguments to create_rectangle
        """
        BasicIGen.__init__(self, width, height, **kwargs)

    def displays_at(self, canvas: tk.Canvas, posn: Posn) -> None:
        """ Draw the Rectangle at the given Position on the Canvas
        :param canvas: The Canvas the image will be drawn on
        :param posn: The position the image will be drawn
        """
        canvas.create_rectangle(*posn, *make_posn(posn, self.width, self.height), **self.kwargs)
