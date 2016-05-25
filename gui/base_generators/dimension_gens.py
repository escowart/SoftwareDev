from gui.base_generators.image_gen import *


class StaticWidthGen(metaclass=ABCMeta):
    """ A interface representing the a Static Image Generator with fixed width
    """

    def __init__(self, width: Natural):
        """ Construct a Static Image Generator with its width
        :param width: The width of the Image
        """
        self._width = None   # type: Natural

        self.width = width

    @property
    def width(self) -> Natural:
        """ Get the width of the Image """
        if self._width is None:
            raise ValueError("width: Not Set")

        return self._width

    @width.setter
    def width(self, width: Natural) -> None:
        """ Set the width of the Image """
        if not is_natural(width):
            raise ValueError("width: Must be Natural, got: {}".format(width))

        self._width = width


class StaticHeightGen(metaclass=ABCMeta):
    """ A interface representing the a Static Image Generator with fixed height
    """

    def __init__(self, height: Natural):
        """ Construct a Static Image Generator with its height
        :param height: The height of the Image
        """
        self._height = None  # type: Natural

        self.height = height

    @property
    def height(self) -> Natural:
        """ Get the height of the Image """
        if self._height is None:
            raise ValueError("height: Not Set")

        return self._height

    @height.setter
    def height(self, height: Natural) -> None:
        """ Set the height of the Image """
        if not is_natural(height):
            raise ValueError("height: Must be Natural, got {}".format(height))

        self._height = height


class StaticDimensions(StaticWidthGen, StaticHeightGen, metaclass=ABCMeta):
    """ A interface representing the a Static Image Generator with fixed width and height
    """

    def __init__(self, width: Natural, height: Natural):
        """ Construct a Static Image Generator with its width and height
        :param width: The width of the Image
        :param height: The height of the Image
        """
        StaticWidthGen.__init__(self, width)
        StaticHeightGen.__init__(self, height)
