from gui.player_gen import *
from gui.base_generators.grid_gens import *
from evolution.dealers.dealer import *


def make_configuration_igen(configuration: Configuration) -> ImageGenerator:
    """ Make a Configuration Image Generator
    :param configuration: The Configuration
    :return: The IGen
    """
    igen = GridSlotsIGen(num_rows=3, num_columns=3)

    num_players = len(configuration.player_sequence)

    for index, player_state in enumerate(configuration.player_sequence):
        posn = posn_on_config_igen(index, num_players)
        player_image = make_player_state_igen(player_state)
        igen.place_at(player_image, posn)

    watering_hole = make_watering_hole_igen(configuration)
    igen.place_at(watering_hole, WATERING_HOLE_POSN)

    return igen


def make_watering_hole_igen(configuration: Configuration) -> ImageGenerator:
    """ Make a Watering Hole IGen from the Configuration
    :param configuration: The Configuration
    :return: The IGen
    """
    deck_igen = make_trait_cards_igen(configuration.deck.cards)
    igen = DynamicRowsIGen(width=deck_igen.width, has_border=True)

    food_igen = TextIGen(deck_igen.width, TEXT_HEIGHT, text="Food Tokens: {}".format(configuration.watering_hole))
    igen.add_row(food_igen)
    igen.add_row(deck_igen)

    return igen


def posn_on_config_igen(index: Index, num_players: Natural) -> Posn:
    """ Get the Posn in the IGen-Configuration for the external_players at the index given the number of players
    :param index: The index of the Player
    :param num_players: The number of players
    :return: The position of the external_players on the IGen
    """
    if index == 0:
        return Posn(1, 2)
    elif index == 1:
        return Posn(2, 2)
    elif index == 2:
        return Posn(2, 1)
    elif index == 3:
        return Posn(2, 0)
    elif index == 4:
        return Posn(1, 0)
    elif index == 5:
        return Posn(0, 0)
    elif index == 6:
        return Posn(0, 1)
    elif index == 7:
        return Posn(0, 2)
    else:
        raise ValueError("posn_on_config_igen: Index must be in (0,8]")
