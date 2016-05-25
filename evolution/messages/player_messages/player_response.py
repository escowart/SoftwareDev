from evolution.messages.message import *

OptPlayerResponse = ['PlayerResponse', InvalidMessageClass]


class PlayerResponse(Response):
    """ A class representing a Response from the Player
    A PlayerResponse is one of:
        - SignUp
        - Action
        - FeedingChoice
    """

    @abstractmethod
    def is_valid(self, dealer: IDealer, player: IPlayer) -> bool:
        """ Is this Player Response from the given player valid?
        :param dealer: The Dealer of the Game
        :param player: The Player whose response is being validated
        """
        raise NotImplementedError("is_valid")

    @abstractmethod
    def apply(self, dealer: IDealer, player: IPlayer) -> None:
        """ Apply the Action of the given player on the dealers
        Effect: Modifies the Dealer and Player according to the Response
        :param dealer: The Dealer of the Game
        :param player: The Player whose response is being validated
        """
        raise NotImplementedError("apply")


class ValidNoPlayerResponseClass(PlayerResponse, ValidNoResponseClass):
    """ A No Response for when message are sent to an external player that require not response """

    def is_valid(self, dealer: IDealer, player: IPlayer) -> bool:
        """ Is this Player Response from the given player valid?
        :param dealer: The Dealer of the Game
        :param player: The Player whose response is being validated
        """
        return True

    def apply(self, dealer: IDealer, player: IPlayer) -> None:
        """ Apply the Action of the given player on the dealers
        Effect: Modifies the Dealer and Player according to the Response
        :param dealer: The Dealer of the Game
        :param player: The Player whose response is being validated
        """
        return

ValidNoPlayerResponse = ValidNoPlayerResponseClass()

