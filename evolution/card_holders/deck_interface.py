from evolution.cards.trait_card_interface import *


class OptDeck(object, metaclass=ABCMeta):
    """ An OptDeck is one of:
        - NoDeck
        - IDeck
    """


class NoDeckClass(OptDeck):
    """ The NO-Deck class """
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, NoDeckClass)

NoDeck = NoDeckClass()


class IDeck(OptDeck, metaclass=ABCMeta):
    """ An interface for a Deck """