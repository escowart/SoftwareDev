from gui.base_generators.basic_gen import *


class OvalIGen(BasicIGen):
    """ A class representing an Oval Image generator """

    def __init__(self,
                 width: Natural,
                 height: Optional[Natural] = None,
                 **kwargs: dict) -> None:
        """ Construct an Oval IGen
        :param width: The width of the Image
        :param height: The height of the Image
        :param kwargs: The extra keyword arguments of the Basic Image Generator
        """
        height = width if (height is None) else height
        BasicIGen.__init__(self, width, height, **kwargs)

    def displays_at(self, canvas: tk.Canvas, posn: Posn) -> None:
        """ Draw the Oval at the given Position on the Canvas
        :param canvas: The Canvas the image will be drawn on
        :param posn: The position the image will be drawn
        """
        end_posn = make_posn(posn, self.width, self.height)

        canvas.create_oval(*posn, *end_posn, **self.kwargs)

    def __repr__(self):
        return "OvalIGen(width={}, height={}, kwargs={})".format(self.width,
                                                                 self.height,
                                                                 self.kwargs)

    def __eq__(self, other):
        if not isinstance(other, OvalIGen):
            return False

        other_oval = cast(OvalIGen, other)
        return ((self.width == other_oval.width) and
                (self.height == other_oval.height) and
                (self.kwargs == other_oval.kwargs))
