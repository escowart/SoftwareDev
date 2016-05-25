from gui.base_generators.circle_gen import *
from gui.base_generators.columns_gens import *

from gui.base_generators.text_gen import *


def make_species_att_igen(width: Natural,
                          height: Natural,
                          text: str,
                          num_tokens: Natural,
                          num_fill_tokens: Natural,
                          fill_color: HexColor):
    igen = ColumnSlotsGenerator(width=width, height=height, num_slots=MAX_NUMBER_DISPLAY_TOKENS + 1)

    text_igen = TextIGen(width=SPECIES_ATTRIBUTE_TEXT_WIDTH, height=igen.height, text=text)
    igen.add_column(text_igen)

    for i in range(num_tokens):
        token_igen = make_token_igen(igen.remaining_slot_width,
                                     igen.height,
                                     fill_color if (i < num_fill_tokens) else None)
        igen.add_column(token_igen)

    return igen


def make_token_igen(width: Natural, height: Natural, fill_color: Optional[HexColor] = None) -> ImageGenerator:
    """ Make a Token IGen
    :param width: The width of the IGen
    :param height: The height of the IGen
    :param fill_color: The optional fill color
    :return: The IGen
    """
    return CenteredCircleIGen(width=width,
                              height=height,
                              fill_color=fill_color)
