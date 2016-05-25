from evolution.all_evo import *


class IClientPlayer(Player, metaclass=ABCMeta):
    """ A client Player which is held by a Proxy Dealer """

    @abstractmethod
    def get_response(self, message) -> PlayerResponse:
        """ Get this Client Player's Response to the given Message
        :param message: The Message
        :return: The Player's Response
        """
        raise NotImplementedError("get_response")


class IProxyDealer(object, metaclass=ABCMeta):
    """ An interface for Proxy Dealer """

    @abstractmethod
    def run_evolution_for_client(self) -> None:
        """ Run the game evolution for the Client """
        raise NotImplementedError("run_evolution_for_client")

    @abstractmethod
    def get_clients_response(self, message) -> PlayerResponse:
        """ Get the Client Player's Response to the given message
        :param message: The Server Message to Client
        :return: The Client Player's Response
        """
        raise NotImplementedError("get_clients_response")

    @abstractmethod
    def receive_message_to_client(self):
        """ Receive the next Message to this Client
        Effect: Modifies the next server message types if valid
        :return: The Server Message to Client of Invalid Message
        """
        raise NotImplementedError("receive_message_to_client")

    @abstractmethod
    def send_sign_up(self) -> None:
        """ Send the Sign Up Message
        Effect: Modifies the next Server Message type accepted
        """
        raise NotImplementedError("send_sign_up")

    @abstractmethod
    def update_client_player(self,
                             player_id:    OptPlayerId = NoPlayerId,
                             species_list: OptSpecies = NoSpecies,
                             food_bag:     OptNatural = NoNatural,
                             hand:         OptList[TraitCard] = NoList) -> None:
        """ Update the Client Player with its field if they are NoValue
        Effect: Updates the Client Player's fields
        :param player_id: The id of Player
        :param species_list: The Species list
        :param food_bag: The food bag of th ePlayer
        :param hand: The hand of the Player
        """
        raise NotImplementedError("update_client_player")

    @property
    @abstractmethod
    def client_player(self) -> IClientPlayer:
        """ Get the Client Player """
        raise NotImplementedError("client_player")

    @client_player.setter
    @abstractmethod
    def client_player(self, client_player: IClientPlayer) -> None:
        """ Set the Client Player """
        raise NotImplementedError("client_player")

    @property
    @abstractmethod
    def next_server_message_types(self) -> List[type]:
        """ Gets next Server Message Type"""
        raise NotImplementedError("next_server_message_types")

    @next_server_message_types.setter
    @abstractmethod
    def next_server_message_types(self, next_server_message_types: List[type]) -> None:
        """ Sets the next Server Message type"""
        raise NotImplementedError("next_server_message_types")
