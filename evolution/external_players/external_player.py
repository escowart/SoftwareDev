from evolution.messages.player_messages.all_player_messages import *


OptExternalPlayer = ['ExternalPlayer', 'NoExternalPlayerClass']


class NoExternalPlayerClass(object):
    """ The No-External Player class """
    def __repr__(self) -> str:
        return "NoExternalPlayer"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, NoExternalPlayerClass)

NoExternalPlayer = NoExternalPlayerClass()


class ExternalPlayer(object, metaclass=ABCMeta):
    """ A class representing an External Player which the Dealer communicates through a Player """

    def send_new_player(self) -> PlayerResponse:
        """ Send the New Player message to the Client
        Effect: Sends a message over the socket to the Client
        """
        return ValidNoPlayerResponse

    def start_turn(self, food_on_watering_hole: Natural) -> PlayerResponse:
        """ Start the Turn by send the external Player their Player's state
        :param food_on_watering_hole: The food on the watering hole
        Effect: Start the Turn by sending the external player this Player's state
        """
        return ValidNoPlayerResponse

    def shut_down(self) -> PlayerResponse:
        """ Shut down this External Player"""
        return ValidNoPlayerResponse

    @abstractmethod
    def choose_feeding(self,
                       num_tokens_on_watering_hole: Natural,
                       other_players:               List[PlayerConfiguration]) -> OptValidFeedingChoice:
        """ Send a Choose Feeding Message to a messages Player and Interpret the Response
        :param num_tokens_on_watering_hole: the number of tokens on the watering hole
        :param other_players: the states of the other players in the game
        :return: The Opt Valid Feeding Choice received from the wire
        """
        raise NotImplementedError("choose_feeding")

    @abstractmethod
    def choose_action(self,
                      before_players: List[PlayerConfiguration],
                      after_players:  List[PlayerConfiguration]) -> OptValidAction:
        """ Send a Choose Action Message to a messages Player and Interpret the Response
        :param before_players: The list of players whose turns preceded this player
        :param after_players: The list of players whose turns are after this player
        :return: Optional Valid Action received from the wire
        """
        raise NotImplementedError("choose_action")

    @property
    @abstractmethod
    def player_id(self) -> int:
        """ This external player's Player id"""
        raise NotImplementedError("player_id")

    @player_id.setter
    @abstractmethod
    def player_id(self, player_id: int) -> None:
        """ Set this external player's Player id"""
        raise NotImplementedError("player_id")

    @property
    @abstractmethod
    def player_configuration(self) -> PlayerConfiguration:
        """ This External Player's Configuration"""
        raise NotImplementedError("give_player_configuration")

    @player_configuration.setter
    @abstractmethod
    def player_configuration(self, player_config: PlayerConfiguration):
        """ Set this External Player's Configuration """
        raise NotImplementedError("give_player_configuration")