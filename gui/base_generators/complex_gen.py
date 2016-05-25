from gui.base_generators.rectangle_gen import *


class ComplexIGen(ImageGenerator, metaclass=ABCMeta):
    """ A class representing a Canvas that can be drawn and draw on by other Canvases
    (0,0) is the Origin of this canvas
    """

    def __init__(self, sub_gens: OptList[GenAtPosn] = NoList, has_border: bool = DEFAULT_HAS_BORDER) -> None:
        """ Construct an ImageGenerator with its
        :param sub_gens: This Image Generator's sub-Generators
        """
        self._sub_gens = None  # type: List[GenAtPosn]
        self._has_border = None  # type: bool

        self.sub_gens = sub_gens
        self.has_border = has_border

    @property
    def sub_gens(self) -> List[GenAtPosn]:
        """ Get the sub-Generators of this Generator """
        if self._sub_gens is None:
            raise ValueError("sub_gens: Not Set")

        return self._sub_gens

    @sub_gens.setter
    def sub_gens(self, sub_gens: OptList[GenAtPosn]) -> None:
        """ Set the sub-Generators of this Generator """
        if sub_gens == NoList:
            sub_gens = []
        if not is_list(sub_gens, GenAtPosn):
            raise ValueError("sub_gens: Must be a Listof[GenAtPosn], got: {}".format(sub_gens))

        self._sub_gens = sub_gens

    @property
    def has_border(self) -> bool:
        """ Get the has border of this Generator """
        if self._has_border is None:
            raise ValueError("has_border: Not Set")

        return self._has_border

    @has_border.setter
    def has_border(self, has_border: bool) -> None:
        if not isinstance(has_border, bool):
            raise ValueError("has_border: Must be a bool, got: {}".format(has_border))

        self._has_border = has_border

    def add_sub_gen(self, sub_gen: ImageGenerator, at_posn: Posn = POSN_ORIGIN) -> None:
        """ Draw the given sub-ImageGenerator on this Image Generator at the given position
        :param sub_gen: The sub generator
        :param at_posn: The position the sub generator will be generated
        """
        self.sub_gens.append(GenAtPosn(sub_gen, at_posn))

    def displays_at(self, canvas: tk.Canvas, posn: Posn) -> None:
        """ Display the Image at the given Position on the Canvas
        :param canvas: The Canvas the image will be drawn on
        :param posn: The position the image will be drawn
        """
        if self.has_border:
            border_rect = RectangleIGen(self.width, self.height, outline=BLACK, border_width=DEFAULT_OUTLINE_WIDTH)
            border_rect.displays_at(canvas, posn)

        [sub_gen.image_gen.displays_at(canvas, sum_posn(sub_gen.posn, posn)) for sub_gen in self.sub_gens]

    def __repr__(self):
        return "ComplexGen(width: {}, height {}, sub_gens: {})".format(self.width, self.height,
                                                                       ", ".join([repr(sub_gen)
                                                                                  for sub_gen in self.sub_gens]))


class StaticDimComplexIGen(ComplexIGen, StaticDimensions, metaclass=ABCMeta):
    """ Class enabling extension of width and height properties for a Complex IGen
    """
    def __init__(self,
                 width: Natural,
                 height: Natural,
                 sub_gens: OptList[GenAtPosn] = NoList,
                 has_border: bool = DEFAULT_HAS_BORDER) -> None:
        """ Construct a Static Dimensions Complex IGen
        :param width: The width of the IGen
        :param height: The height of the IGen
        :param sub_gens: The sub Generators
        :param has_border: Does it have a border
        """
        ComplexIGen.__init__(self, sub_gens, has_border)
        StaticDimensions.__init__(self, width, height)
