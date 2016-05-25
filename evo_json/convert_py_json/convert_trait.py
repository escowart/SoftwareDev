from evolution.cards.all_cards import *

'''----------- PyJSON Trait <-> TraitCard -----------'''


def is_pj_trait(value: Any) -> bool:
    """ Is the given value a PJ_Trait?
    :param value: THe value being checked
    :return: True if value is a PJ_TRAIT, False otherwise
    """
    return isinstance(value, str) and (value in trait_dictionary.keys())


def convert_from_py_trait(pj_trait: PyJSON) -> TraitCard:
    """ Convert the given PyJSON Trait to a TraitCard
    :param pj_trait: The PyJSON Trait being converted
    :return: The resulting TraitCard
    """
    if not is_pj_trait(pj_trait):
        raise ValueError("convert_from_py_trait: Invalid PyJSON Trait: " + repr(pj_trait))

    return trait_dictionary[pj_trait]()


def convert_to_py_trait(trait_card: TraitCard) -> PyJSON:
    """ Convert the given TraitCard to a PyJSON Trait
    :param trait_card: The TraitCard being converted
    :return: The resulting PyJSON Trait
    """
    if not isinstance(trait_card, TraitCard):
        raise ValueError("convert_to_py_trait: Invalid TraitCard")

    for key, trait_card_subtype in trait_dictionary.items():
        if isinstance(trait_card, trait_card_subtype):
            return key

    # Should not be Reached
    raise ValueError("convert_to_py_trait: Invalid TraitCard, got: " + repr(feeding))


'''----------- PyJSON LOT <-> List[TraitCard] -----------'''


PJ_LOT = List[PyJSON]


def is_pj_lot(value: Any) -> bool:
    """ Is the given value a Py_LOT
    :param value: The value being checked
    :return: True if the value is a Py_LOT, False otherwise
    """
    return isinstance(value, list)


def convert_from_pj_lot(py_lot: PJ_LOT) -> List[TraitCard]:
    """ Convert the given PyJSON LOT to a List of TraitCard
    :param py_lot: The PyJSON LOT being converted
    :return: The resulting List of TraitCard
    """
    if not is_pj_lot(py_lot):
        raise ValueError("convert_from_lot:  Invalid PyJSON LOT, got: {}".format(py_lot))

    return [convert_from_py_trait(py_trait) for py_trait in py_lot]


def convert_to_pj_lot(trait_card_list:  List[TraitCard]) -> PJ_LOT:
    """ Convert the given List of TraitCard to a
    :param trait_card_list: The List of TraitCard being converted
    :return: The resulting LOT
    """
    if not is_list(trait_card_list, TraitCard):
        raise ValueError("convert_to_py_lot: Invalid List[TraitCard], got: {}".format(trait_card_list))

    return [convert_to_py_trait(trait_card) for trait_card in trait_card_list]


'''----------- PyJSON SpeciesCard <-> TraitCard -----------'''


def is_species_card(py_json: PyJSON) -> bool:
    """ Is the given PyJSON a Species Card?
    :param py_json: The PyJSON
    :return: True if the given PyJSON is a Species Card, False otherwise
    """
    return is_list(py_json, length=PJ_SPECIES_CARD_LEN) and isinstance(py_json[0], int) and is_pj_trait(py_json[1])


def convert_from_pj_species_card(py_json: PyJSON) -> TraitCard:
    """ Convert from a PyJSON SpeciesCard to a TraitCard
    :param py_json: Species Card
    :return: Trait Card
    """
    if not is_species_card(py_json):
        raise ValueError("convert_from_pj_species_card: Must be PyJSON SpeciesCard, got: {}".format(py_json))

    food = py_json[0]
    trait = py_json[1]
    return trait_dictionary[trait](food)


def convert_to_pj_species_card(trait_card: TraitCard) -> PyJSON:
    """ Convert from a TraitCard to a SpeciesCard
    :param py_json: Trait Card
    :return: Species Card
    """
    if not isinstance(trait_card, TraitCard):
        raise ValueError("convert_tp_pj_species_card: Must be TraitCard, got: {}".format(feeding))

    food = trait_card.food_card_tokens
    trait = convert_to_py_trait(trait_card)
    return [food, trait]


'''----------- LOC <-> List[TraitCard] -----------'''


def is_loc(py_json: PyJSON) -> bool:
    """ Is the given PyJSON a List of Species Card?
    :param py_json: The PyJSON
    :return: True if the given PyJSON is a List of Species Card, False otherwise
    """
    return isinstance(py_json, list)


def convert_from_pj_loc(py_loc: PyJSON) -> List[TraitCard]:
    """ Convert from a PyJSON List of SpeciesCard to a List of TraitCard
    :param py_loc: List of Species Card
    :return: List of Trait Card
    """
    if not is_loc(py_loc):
        raise ValueError("convert_from_pj_loc: Must be PyJSON Listof[SpeciesCard], got: {}".format(py_loc))

    return [convert_from_pj_species_card(species_card) for species_card in py_loc]


def convert_to_pj_loc(trait_cards: List[TraitCard]) -> PyJSON:
    """ Convert from a List of TraitCard to a List of SpeciesCard
    :param trait_cards: The Trait Cards being converted
    :return: List of Species Card
    """
    if not is_list(trait_cards, of_type=TraitCard):
        raise ValueError("convert_to_pj_loc: Must be Listof[TraitCard], got: {}".format(trait_cards))

    return [convert_to_pj_species_card(trait_card) for trait_card in trait_cards]
