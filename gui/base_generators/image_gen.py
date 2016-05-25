from gui.data_def import *


class GenAtPosn(object):
    """ A class representing a Image which will generated at the position
    """
    def __init__(self, image_gen: 'ImageGenerator', posn: Posn) -> None:
        """ Generate the Image at the given position on the Canvas the Generator which holds this creates.
        :param image_gen: The Image Generator
        :param posn: The position the image will be generated
        """
        self._image_gen = None  # type: ImageGenerator
        self._posn = Posn       # type: Posn

        self.image_gen = image_gen
        self.posn = posn

    def __repr__(self) -> str:
        return "{} @ {}".format(self.image_gen, self.posn)


class ImageGenerator(object, metaclass=ABCMeta):
    """ A interface representing the all ImageGenerator which are either Base or Complex
    """

    @property
    def center_x(self) -> Natural:
        """ Get half of the width """
        return int(self.width / 2)

    @property
    def center_y(self) -> Natural:
        """ Get half of the height """
        return int(self.height / 2)

    @property
    def center(self) -> Posn:
        """ Get the center position of this Image """
        return Posn(self.center_x, self.center_y)

    @property
    def center_left(self) -> Posn:
        """ Get the center left position of this Image """
        return Posn(POSN_ORIGIN.x, self.center_y)

    @property
    def center_right(self) -> Posn:
        """ Get the center right position of this Image """
        return Posn(self.width, self.center_y)

    @property
    def center_top(self) -> Posn:
        """ Get the center top position of this Image """
        return Posn(self.center_x, POSN_ORIGIN.y)

    @property
    def center_bottom(self) -> Posn:
        """ Get the center right position of this Image """
        return Posn(self.center_x, self.height)

    @property
    def top_left(self) -> Posn:
        """ Get the top left position of this Image """
        return POSN_ORIGIN

    @property
    def top_right(self) -> Posn:
        """ Get the top right position of this Image """
        return Posn(self.width, POSN_ORIGIN.y)

    @property
    def bottom_left(self) -> Posn:
        """ Get the top left position of this Image """
        return Posn(POSN_ORIGIN.x, self.height)

    @property
    def bottom_right(self) -> Posn:
        """ Get the top right position of this Image """
        return Posn(self.width, self.height)

    def display(self, root) -> None:
        """ Generate the Image on a Empty Canvas
        :param root: The root display
        """
        canvas = tk.Canvas(root, width=self.width, height=self.height, highlightthickness=DEFAULT_HEIGHT_THICKNESS,
                           bg=WHITE)
        xsb = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
        ysb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        canvas.configure(xscrollcommand=xsb.set, yscrollcommand=ysb.set)
        canvas.configure(scrollregion= canvas.bbox("all"))
        canvas.bind("<ButtonPress-1>", lambda event, arg=canvas: self.scroll_start(event, arg))
        canvas.bind("<B1-Motion>", lambda event, arg=canvas: self.scroll_move(event, arg))
        canvas.grid()
        self.displays_at(canvas, POSN_ORIGIN)

    @abstractmethod
    def displays_at(self, canvas: tk.Canvas, posn: Posn) -> None:
        """ Display the Image at the given Position on the Canvas
        :param canvas: The Canvas the image will be drawn on
        :param posn: The position the image will be drawn
        """
        raise NotImplementedError("_draw_at")

    def __repr__(self):
        return "ImageGen(width: {}, height: {})".format(self.width, self.height)

    @staticmethod
    def scroll_start(event, canvas: tk.Canvas) -> None:
        """ Records x and y and the canvas's current view
        :param event: Position of the mouse click
        :param canvas: The Canvas the image is drawn on
        """
        canvas.scan_mark(event.x, event.y)

    @staticmethod
    def scroll_move(event, canvas: tk.Canvas) -> None:
        """ Computes the difference between mouse coordinates
        and the x and y arguments to the last scanMark method for the widget.
        :param event: Position of where the mouse was dragged to
        :param canvas: The Canvas the image is drawn on
        """
        canvas.scan_dragto(event.x, event.y, gain=1)
