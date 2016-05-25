from evo_json.convert_py_json.convert_species import *

'''----------- PyJSON Player id field <-> Natural -----------'''


PJ_Id = List[PyJSON]  # of format ["id", NaturalPlus]


def is_pj_id(value: Any) -> bool:
    """ IS the given value a PJ_Id?
    :param value: The value being checked
    :return: True if given value is a PJ_Id, False otherwise
    """
    return is_list(value, length=PJ_FIELD_LEN) and (value[0] == ID_STR) and is_natural_plus(value[1])


def convert_from_id(pj_id: PJ_Id) -> NaturalPlus:
    """ Convert the given PJ_ID to a NaturalPlus id
    :param pj_id: The PJ_Id being converted
    :return: The resulting NaturalPlus id
    """
    if not is_pj_id(pj_id):
        raise ValueError("convert_from_id: Invalid PyJSON Id, got: {}".format(pj_id))

    return pj_id[1]


def convert_to_pj_id(id_nat_plus: NaturalPlus) -> PJ_Id:
    """ Convert the given NaturalPlus id to a PJ_ID
    :param id_nat_plus: The NaturalPlus id being converted
    :return: The resulting PJ_ID
    """
    if not is_natural_plus(id_nat_plus):
        raise ValueError("convert_to_pj_id: Not given Natural+, got: {}".format(id_nat_plus))

    return [ID_STR, id_nat_plus]


'''----------- PyJSON Player species field <-> Listof[Species] -----------'''


PJ_Player_Species = List[PyJSON] # of format ["species", PJ_LOS]


def is_pj_player_species(value: Any):
    """ Is the given value a PJ_Player_Species
    :param value: The value being checked
    :return: True if value is a PJ_Player_Species, False otherwise
    """
    return is_list(value, length=PJ_FIELD_LEN) and (value[0] == SPECIES_STR) and isinstance(value[1], list)


def convert_from_pj_player_species(pjp_species: PJ_Player_Species) -> List[Species]:
    """ Convert the given PJ_Player_Species to a Listof[Species]
    :param pjp_species: PJ_Player_Species
    :return: The Listof[Species]
    """
    if not is_pj_player_species(pjp_species):
        raise ValueError("convert_from_pj_player_species: Invalid PyJSON SimplePlayer Species, got: {}".format(pjp_species))

    return convert_from_pj_los(pjp_species[1])


def convert_to_pj_player_species(species_list: List[Species]) -> PJ_Player_Species:
    """ Convert the given Listof[Species] a PJ_Player_Species
    :param species_list: Listof[Species]
    :return: The PJ_Player_Species
    """

    return [SPECIES_STR, convert_to_pj_los(species_list)]

'''----------- PyJSON Player bag field <-> Natural -----------'''

PJ_Bag = List[PyJSON]  # of format ["bag", Natural]


def is_pj_bag(value: Any) -> bool:
    """ IS the given value a PJ_ID?
    :param value: The value being checked
    :return: True if given value is a PJ_ID, False otherwise
    """
    return is_list(value, length=PJ_FIELD_LEN) and (value[0] == BAG_STR) and is_natural(value[1])


def convert_from_bag(pj_bag: PJ_Bag) -> Natural:
    """ Convert the given PJ_Bag to a Natural
    :param pj_bag: The PJ_Bag being converted
    :return: The resulting Natural
    """
    if not is_pj_bag(pj_bag):
        raise ValueError("convert_from_bag: Invalid PyJSON Bag, got: {}".format(pj_bag))

    return pj_bag[1]


def convert_to_pj_bag(bag_nat: Natural) -> PJ_Bag:
    """ Convert the given NaturalPlus bag_nat to a PJ_Bag
    :param bag_nat: The NaturalPlus bag_nat being converted
    :return: The resulting PJ_Bag
    """
    if not is_natural(bag_nat):
        raise ValueError("convert_to_pj_bag: Not given Natural, got: {}".format(feeding))

    return [BAG_STR, bag_nat]


'''----------- PyJSON Player cards field <-> Natural -----------'''

PJ_Cards = List[PyJSON]  # of format ["card", Listof[SpeciesCard]]


def is_pj_cards(value: Any) -> bool:
    """ IS the given value a PJ_Cards?
    :param value: The value being checked
    :return: True if given value is a PJ_Cards, False otherwise
    """
    return is_list(value, length=PJ_FIELD_LEN) and (value[0] == CARDS_STR)


def convert_from_pj_cards(pj_cards: PJ_Cards) -> List[TraitCard]:
    """ Convert the given PJ_Cards to a Natural
    :param pj_cards: The PJ_Cards being converted
    :return: The resulting Listof[TraitCard]
    """
    if not is_pj_cards(pj_cards):
        raise ValueError("convert_from_cards: Invalid PyJSON Cards, got: {}".format(pj_cards))

    return convert_from_pj_loc(pj_cards[1])


def convert_to_pj_cards(trait_cards: List[TraitCard]) -> PJ_Cards:
    """ Convert the given Listof[TraitCard] bag_nat to a PJ_Cards
    :param trait_cards: The Listof[TraitCard] bag_nat being converted
    :return: The resulting PJ_Cards
    """
    if not is_list(trait_cards, of_type=TraitCard):
        raise ValueError("convert_to_pj_cards: Not given Listof[TraitCard], got: {}".format(trait_cards))

    return [CARDS_STR, convert_to_pj_loc(trait_cards)]