from gui.base_generators.basic_gen import *


class CenteredCircleIGen(BasicIGen):
    """ A circle Generator which can be align on the rectangle canvas """

    def __init__(self,
                 width: Natural,
                 height: Natural,
                 radius: Optional[Natural] = None,
                 **kwargs: dict) -> None:
        """
        :param width: The width of the transparent Rectangle the Circle is being drawn on
        :param height: The height of the transparent Rectangle the Circle is being drawn on
        :param radius: The radius of the Circle
        :param kwargs: The extra keyword arguments of the Circle Generator
        """
        radius = int(min(width, height) / 2) if (radius is None) else radius

        BasicIGen.__init__(self, width, height, **kwargs)

        self._radius = None  # type: Natural

        self.radius = radius

    @property
    def radius(self) -> Natural:
        """ Get the radius of this Circle """
        if self._radius is None:
            raise ValueError("radius: Not Set")

        return self._radius

    @radius.setter
    def radius(self, radius: Natural) -> None:
        """ Set the radius of this Circle """
        if not is_natural(radius):
            raise ValueError("radius: Must be Natural, got: {}".format(radius))

        self._radius = radius

    def displays_at(self, canvas: tk.Canvas, posn: Posn) -> None:
        """ Draw the Circle at the given Position on the Canvas
        :param canvas: The Canvas the image will be drawn on
        :param posn: The position the image will be drawn
        """
        center = sum_posn(self.center, posn)

        canvas.create_oval(*make_posn(center, -self.radius, -self.radius),
                           *make_posn(center, self.radius, self.radius),
                           **self.kwargs)
