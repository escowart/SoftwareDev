from gui.base_generators.grid_gens import *
from gui.species_gen import *
from gui.trait_card_gen import *
from evolution.player.player import *


def make_player_state_igen(player_state: Player):
    """ Make a PlayerState IGen
    :param player_state: THe Player State
    :return: The IGen
    """
    igen = DynamicRowsIGen(width=PLAYER_IMAGE_WIDTH, has_border=True)

    id_food_bag_igen = make_id_food_bag_igen(player_state, igen.width)

    igen.add_row(id_food_bag_igen)

    species_list_igen = make_species_list_igen(player_state)
    igen.add_row(species_list_igen)

    if not player_state.is_hand_empty:
        hand_igen = make_trait_cards_igen(player_state.hand)
        igen.add_row(hand_igen)

    return igen


def make_id_food_bag_igen(player_state: Player, width: Natural) -> ImageGenerator:
    """ Make a PlayerState's Id and Food Bag IGen
    :param player_state: The PlayerState
    :param width: The width of the IGen
    :return: The IGen
    """
    return TextIGen(width=width,
                    height=TEXT_HEIGHT,
                    text="ID: {} \t Food Bag: {}".format(player_state.player_id, player_state.food_bag))


def make_species_list_igen(player_state: Player) -> ImageGenerator:
    """ Make a Species List IGen from the PlayerState
    :param player_state: The PlayerState
    :return: The IGen
    """
    igen = GridIGen(width=PLAYER_IMAGE_WIDTH,
                    row_height=SPECIES_IMAGE_ATTRIBUTE_HEIGHT * 3,
                    num_slots_per_row=NUM_SPECIES_IMAGE_SLOTS,
                    has_border=True)

    for species in player_state.species_list:
        igen.add_to_next_column_slot(make_species_igen(species))

    return igen


