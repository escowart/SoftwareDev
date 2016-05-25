from gui.base_generators.rows_gens import *
from gui.species_att_gen import *
from evolution.species.species import *


def make_species_igen(species: Species) -> ImageGenerator:
    """ Make an Image Generator from the given Species
    :param species: The Species
    :return: The Image Generator
    """
    igen = DynamicRowsIGen(width=SPECIES_IMAGE_WIDTH, has_border=True)

    population_igen = make_population_igen(species, igen.width)
    igen.add_row(population_igen)

    body_igen = make_body_igen(species, igen.width)
    igen.add_row(body_igen)

    if species.any_traits:
        traits_igen = make_traits_igen(species, igen.width)
        igen.add_row(traits_igen)

    return igen


def make_population_igen(species: Species, width: Natural) -> ImageGenerator:
    """ Make a population IGen from the Species
    :param species: The Species
    :param width: The width of the IGen
    :return: The IGen
    """
    return make_species_att_igen(width=width,
                                 height=SPECIES_IMAGE_ATTRIBUTE_HEIGHT,
                                 text=POP_STR,
                                 num_tokens=species.population,
                                 num_fill_tokens=species.fed_food,
                                 fill_color=GREEN)


def make_body_igen(species: Species, width: Natural) -> ImageGenerator:
    """ Make a Body Size IGen from the given Species
    :param species: The Species
    :param width: The width of the IGen
    :return: The IGen
    """
    return make_species_att_igen(width=width,
                                 height=SPECIES_IMAGE_ATTRIBUTE_HEIGHT,
                                 text=BODY_STR,
                                 num_tokens=species.body_size,
                                 num_fill_tokens=(species.stored_fat_food
                                                  if species.has_fat_tissue else 0),
                                 fill_color=YELLOW)


def make_traits_igen(species: Species, width: Natural) -> ImageGenerator:
    """ Make a Traits IGen
    :param species: The Species
    :param width: The width of the IGen
    :return: The IGen
    """
    traits_igen = ColumnSlotsGenerator(width=width,
                                       height=SPECIES_IMAGE_ATTRIBUTE_HEIGHT,
                                       num_slots=species.num_traits)

    for trait_card in species.trait_cards:
        trait_text = make_trait_text_igen(trait_card, traits_igen.remaining_slot_width, traits_igen.height)
        traits_igen.add_column(trait_text)

    return traits_igen


def make_trait_text_igen(trait_card: TraitCard, width: Natural, height: Natural) -> ImageGenerator:
    """ Make a TraitCard Text IGen
    :param trait_card: The Trait Card
    :param width: The width of the IGen
    :param height: The height of the IGen
    :return: The IGen
    """
    return TextIGen(width=width,
                    height=height,
                    text=trait_card.name)
