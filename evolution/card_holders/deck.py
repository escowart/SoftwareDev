from evolution.cards.all_cards import *
from evolution.card_holders.lexicographic_card_key import *

class Deck(IDeck):
    """ The Deck of the Game """
    def __init__(self, cards: OptList[ITraitCard] = NoList):
        """ Construct the Deck of the Game
        :param cards: The List of Cards in the Game
        """
        self._cards = Unset  # type: List[ITraitCard]

        self.cards = cards

    @property
    def cards(self) -> List[ITraitCard]:
        """ Get the cards of this deck """
        return assert_set(self._cards)

    @cards.setter
    def cards(self, cards: OptList[ITraitCard]) -> None:
        """ Set the cards of this deck """
        if cards == NoList:
            cards = []

        assert_type(cards, list, of_type=ITraitCard, func_name="cards")
        self._cards = cards

    def __len__(self) -> Natural:
        """Returns the length of the deck"""
        return len(self.cards)

    def draw_cards(self, num_cards: NaturalPlus) -> List[ITraitCard]:
        """Draw from the deck a given amount of cards
        :Effect Removes the number of cards given from the deck
        :param num_cards: The number of cards to remove
        :return: List of the drawn cards
        """
        num_cards_draw = min(num_cards, len(self))
        return_cards = []

        for i in range(num_cards_draw):
            return_cards += [self.cards.pop(DEFAULT_START_INDEX)]

        return return_cards

    def draw_card(self) -> TraitCard:
        """ Draw a card from the deck
        Effect: Removes the drawn card from the deck
        """
        return self.cards.pop(DEFAULT_START_INDEX)

    def order(self, key: type(OrderedKey)) -> None:
        """ Orders the Deck according to the key
        Effect: Modifies the Deck order
        :param key: The specification of how the Deck should be ordered
        """
        self.cards.sort(key=key)
        self.cards.reverse()

    @staticmethod
    def create_deck() -> 'Deck':
        """ Creates a deck with all the cards in it
        :return: Deck with all necessary cards
        """
        all_cards = []
        for trait_type in trait_dictionary.values():
            all_cards += trait_type.create_all_cards(trait_type)

        deck = Deck(all_cards)
        deck.order(LexicographicCardKey)

        return deck



    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Deck) and (self.cards == cast(Deck, other).cards)

    def __repr__(self) -> str:
        return "Deck({})".format(self.cards)
