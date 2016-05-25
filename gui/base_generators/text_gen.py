from gui.base_generators.basic_gen import *


class TextIGen(BasicIGen):
    """ A class representing a Text Image Generator
    """
    def __init__(self,
                 width: Natural,
                 height: Natural,
                 text: str,
                 **kwargs: dict) -> None:
        """ Construct a text
        :param width: The width of the text box
        :param height: The height of the text box
        :param text: The text
        :param kwargs: The keyword arguments to create_text
        """
        kwargs[TEXT_STR] = text
        BasicIGen.__init__(self, width, height, **kwargs)

    def displays_at(self, canvas: tk.Canvas, posn: Posn) -> None:
        """ Draw the Rectangle at the given Position on the Canvas
        :param canvas: The Canvas the image will be drawn on
        :param posn: The position the image will be drawn
        """
        canvas.create_text(*sum_posn(self.center, posn), **self.kwargs)
