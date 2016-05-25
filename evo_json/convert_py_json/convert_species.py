from evo_json.convert_py_json.convert_species_fields import *
from evolution.species.all_species import *

"""----------- PyJSON Species <-> Species -----------"""


PJ_Species = List[PyJSON]  # of format [PJ_Food, PJ_Body, PJ_Pop, PJ_Traits]


def is_pj_species(value: Any):
    """ Is the given value a PyJSON Species?
    :param value: The value being checked
    :return: True if the given value is a PyJSON Species
    """
    return is_list(value, length=PJ_SPECIES_LEN)


def convert_from_pj_species(species: PyJSON) -> Species:
    """ Convert the given PyJSON Species to a Species
    :param species: The PyJSON Species being converted
    :return: The Species

    """
    if not is_pj_species(species):
        raise ValueError("convert_species: Invalid PyJSON Species, got: {}".format(species))

    return Species(convert_from_pj_food(species[0]),
                   convert_from_pj_body(species[1]),
                   convert_from_pj_pop(species[2]),
                   convert_from_pj_traits(species[3]))


def convert_to_pj_species(species: Species) -> PyJSON:
    """ Convert the given Species to a PyJSON Species
    :param species: The Species being converted
    :return: The PyJSON Species

    Species = [food, body, population, traits]
    """
    if not isinstance(species, Species):
        raise ValueError("convert_species: Invalid Species, got: " + repr(species))

    return [convert_to_pj_food(species.fed_food),
            convert_to_pj_body(species.body_size),
            convert_to_pj_pop(species.population),
            convert_to_pj_traits(species.trait_cards)]


"""----------- PyJSON OptSpecies <-> Optional[Species] -----------"""


PJ_OptSpecies = PyJSON  # one of False or PJ_Species


def is_pj_opt_species(value: Any):
    """ Is the given value a PyJSON OptSpecies?
    :param value: The value being checked
    :return: True if the given value is a PyJSON OptSpecies
    """
    return (value == PJ_OPT) or is_pj_species(value)


def convert_from_pj_opt_species(pj_opt_species: PJ_OptSpecies) -> OptSpecies:
    """ Convert the given PyJSON OptSpecies to a Optional Species
    :param species: The PyJSON OptSpecies being converted
    :return: The Optional Species
    """
    if pj_opt_species == PJ_OPT:
        return NoSpecies
    else:
        return convert_from_pj_species(pj_opt_species)


def convert_to_pj_opt_species(opt_species: OptSpecies=NoSpecies) -> PJ_OptSpecies:
    """ Convert the given Optional Species to a PyJSON OptSpecies
    :param species: The Optional Species being converted
    :return: The PyJSON OptSpecies

    OptSpecies is either Species or False
    """
    if opt_species == NoSpecies:
        return PJ_OPT
    else:
        return convert_to_pj_species(cast(Species, opt_species))


"""----------- PyJSON Species+ <-> Species -----------"""


PJ_Species_Plus = List[PyJSON]  # of format [PJ_Food, PJ_Body, PJ_Pop, PJ_Traits, PJ_Fat_Food]


def is_pj_species_plus(value: Any):
    """ Is the given value a PyJSON Species+?
    :param value: The value being checked
    :return: True if the given value is a PyJSON Species+
    """
    return is_list(value, with_len=PJ_SPECIES_PLUS_LEN)


def convert_from_pj_species_plus(pj_species: PyJSON) -> Species:
    """ Convert the given PyJSON Species+ to a Species
    :param pj_species: The PyJSON Species+ being converted
    :return: The Species

    Species+ = [food, body, population, traits, fat-food]
    """
    if is_list(pj_species, length=PJ_SPECIES_LEN):  # Is Normal Species
        return convert_from_pj_species(pj_species)
    elif not is_list(pj_species, length=PJ_SPECIES_PLUS_LEN):
        raise ValueError("convert_from_pj_species_plus: Invalid PyJSON Species+: {}".format(pj_species))

    species = Species(fed_food=convert_from_pj_food(pj_species[0]),
                      body_size=convert_from_pj_body(pj_species[1]),
                      population=convert_from_pj_pop(pj_species[2]),
                      played_cards=convert_from_pj_traits(pj_species[3]))

    if not species.has_fat_tissue:
        raise ValueError("convert_from_pj_species_plus: PJ Species has fat-tissue field "
                         "with no Fat Tissue Trait, got: {}".format(pj_species))

    species.stored_fat_food = convert_from_pj_fat_food(pj_species[PJ_SPECIES_LEN])
    return species


def convert_to_pj_species_plus(species: Species) -> PyJSON:
    """ Convert the given Species to a PyJSON Species+
    :param species: The Species being converted
    :return: The PyJSON Species+

    Species+ = [food, body, population, traits, fat-food]
    """

    base_species = convert_to_pj_species(species)

    if species.has_stored_food:
        base_species.append(convert_to_pj_fat_food(species.stored_fat_food))

    return base_species


"""----------- PyJSON LOS <-> Listof[Species] -----------"""


def is_pj_los(value: Any):
    """ Is the given value a PyJSON Listof Species+?
    :param value: The value being checked
    :return: True if the given value is a PyJSON Listof Species+
    """
    return isinstance(value, list)


def convert_from_pj_los(py_los: PyJSON) -> List[Species]:
    """ Convert PyJSON LOS into a List of Species
    :param py_los: The  PyJSON LOS being converted
    :return: The resulting List of Species
    """
    if not is_pj_los(py_los):
        raise ValueError("convert_species_plus_list: Invalid PyJSON LOS, got {}".format(py_los))

    return [convert_from_pj_species_plus(py_species_plus) for py_species_plus in py_los]


def convert_to_pj_los(species_plus_list: List[Species]) -> PyJSON:
    """ Convert List of Species into a PyJSON LOS
    :param species_plus_list: The  List of Species being converted
    :return: The resulting PyJSON PyJSON LOS
    """
    if not is_list(species_plus_list, Species):
        raise ValueError("convert_species_plus_list: Invalid Listof[Species], got {}".format(species_plus_list))

    return [convert_to_pj_species_plus(species_plus) for species_plus in species_plus_list]
