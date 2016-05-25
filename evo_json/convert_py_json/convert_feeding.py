from evo_json.convert_py_json.convert_player import *

"""----------- PyJSON Feeding <-> Feeding -----------"""


PJ_Feeding = List[PyJSON]  # of format [PJ_Player, PJ_Watering_Hole, Listof[PJ_Player]]


def is_pj_feeding(value: Any):
    """ Is the given value a PJ_Feeding
    :param value: The value
    :return: True if value is a PJ_Feeding, False otherwise
    """
    return is_list(value, length=PJ_FEEDING_LEN)


def convert_from_pj_feeding(pj_feeding: PJ_Feeding) -> Feeding:
    """ Convert the given PJ_Feeding to Feeding
    :param pj_feeding: PJ_Feeding
    :return: Feeding
    """
    if not is_pj_feeding(pj_feeding):
        raise ValueError("convert_from_pj_feeding: Invalid PyJSON Feeding, got: {}".format(pj_feeding))

    return Feeding(player=convert_from_pj_player(pj_feeding[0]),
                   watering_hole=pj_feeding[1],
                   other_players=convert_from_pj_lop(pj_feeding[2]))


def convert_feeding_choice_to_pj(feeding_choice: DataFeedingChoice) -> PyJSON:
    """
    Converts the given evolution choice into the equivalent PyJSON
    :param feeding_choice:
    :return:
    """
    if isinstance(feeding_choice, DataForgoChoice):
        return False
    if isinstance(feeding_choice, DataFeedVegetarian):
        return convert_to_pj_species_plus(feeding_choice.vegetarian)
    if isinstance(feeding_choice, DataStoreFat):
        return [convert_to_pj_species_plus(feeding_choice.species), feeding_choice.num_food_to_store]
    if isinstance(feeding_choice, DataAttackWithCarnivore):
        return [convert_to_pj_species_plus(feeding_choice.carnivore),
                convert_to_pj_player(feeding_choice.target_player),
                convert_to_pj_species_plus(feeding_choice.target_species)]


def convert_player_feeding_choice_to_pj(player_feeding_choice: FeedingChoice) -> PyJSON:
    """
    Converts the given external_players evolution choice into the equivalent PyJSON
    :param player_feeding_choice: The SimplePlayer Feeding Choice
    :return: The resulting PyJSON
    """
    if isinstance(player_feeding_choice, ForgoChoice):
        return False
    if isinstance(player_feeding_choice, FeedVegetarianChoice):
        return player_feeding_choice.vegetarian_index
    if isinstance(player_feeding_choice, StoreFatChoice):
        return [player_feeding_choice.species_index,
                player_feeding_choice.num_food_to_store]
    if isinstance(player_feeding_choice, AttackWithCarnivoreChoice):
        return [player_feeding_choice.carnivore_index,
                player_feeding_choice.target_player_index,
                player_feeding_choice.target_species_index]


def convert_to_pj_feeding(feeding: Feeding) -> PJ_Feeding:
    """ Convert the given Feeding to PJ_Feeding
    :param feeding: Feeding
    :return: PJ_Feeding
    """
    if not isinstance(feeding, Feeding):
        raise ValueError("convert_to_pj_feeding: Invalid Feeding, got: {}".format(feeding))

    return [convert_to_pj_player(feeding.player_state),
            feeding.watering_hole,
            convert_to_pj_lop(feeding.other_player_states)]



