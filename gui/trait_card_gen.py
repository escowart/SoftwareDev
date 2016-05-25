from gui.base_generators.rows_gens import *
from gui.base_generators.text_gen import *
from gui.base_generators.grid_gens import *
from evolution.cards.trait_card import *


def make_trait_card_igen(trait_card: TraitCard) -> ImageGenerator:
    """ Make the given TraitCard into an Image Generator
    :param trait_card: The TraitCard
    :return: The Image Generator
    """
    igen = DynamicRowsIGen(width=TRAIT_CARD_IMAGE_WIDTH, has_border=True)

    trait_text_igen = make_trait_text_igen(trait_card, igen.width)
    igen.add_row(trait_text_igen)

    food_text_igen = make_food_text_igen(trait_card, igen.width)
    igen.add_row(food_text_igen)

    return igen


def make_trait_text_igen(trait_card: TraitCard, width: Natural) -> ImageGenerator:
    """ Make the text of the given TraitCard into an Image Generator
    :param trait_card: The TraitCard
    :param width: The width
    :return: The Trait Text Image Generator
    """
    return TextIGen(width=width, height=TEXT_HEIGHT, text=trait_card.name)


def make_food_text_igen(trait_card: TraitCard, width: Natural) -> ImageGenerator:
    """ Make the food of the given TraitCard into an Image Generator
    :param trait_card: The TraitCard
    :param width: The width
    :return: The Food Text Image Generator
    """
    return TextIGen(width=width, height=TEXT_HEIGHT, text="Food Tokens: {}".format(trait_card.food_card_tokens))


def make_trait_cards_igen(trait_cards: List[TraitCard]) -> ImageGenerator:
    """ Make a Hand IGen from the TraitCards
    :param trait_cards: The TraitCards
    :return: The IGen
    """
    igen = GridIGen(width=PLAYER_IMAGE_WIDTH,
                    row_height=TEXT_HEIGHT * 2,
                    num_slots_per_row=NUM_TRAIT_CARD_IMAGE_SLOTS,
                    has_border=True)

    for trait_card in trait_cards:
        igen.add_to_next_column_slot(make_trait_card_igen(trait_card))

    return igen


