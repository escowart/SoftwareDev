from gui.base_generators.dimension_gens import *


class BasicIGen(ImageGenerator, StaticDimensions, metaclass=ABCMeta):
    """ A class representing a basic image generator which constructs the actual images to be generated
    """

    def __init__(self,
                 width: Natural,
                 height: Natural,
                 fill_color: Optional[HexColor] = None,
                 border_width: Optional[Natural] = None,
                 **kwargs: dict) -> None:
        """
        :param width: The width of the Image
        :param height: The height of the Image
        :param align: The align of the Image on it's rectangular backdrop
        :param fill_color: The fill of the Image
        :param border_width: The border width of the Image
        :param kwargs: The extra keyword arguments of the Image
        """
        ImageGenerator.__init__(self)
        StaticDimensions.__init__(self, width, height)

        if fill_color is not None:
            kwargs[FILL_STR] = fill_color
        if border_width is not None:
            kwargs[BORDER_WIDTH_STR] = border_width

        self.kwargs = kwargs


