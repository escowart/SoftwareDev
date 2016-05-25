from evolution.messages.messages_to_client.all_message_to_client import *
from evolution.messages.player_messages.sign_up_message import *
from evolution.messages.message_socket import *


class ClientPlayer(IClientPlayer):
    """ A client Player which is held by a Proxy Dealer """

    def __init__(self, external_player_type: type(ExternalPlayer), player_name: OptStr = NoStr) -> None:
        """ Construct a Client Player
        :param external_player_type: The type of External Player
        """
        Player.__init__(self, NO_ID, external_player_type=external_player_type, player_name=player_name)

    def get_response(self, message: ServerMessageToClient) -> PlayerResponse:
        """ Get this Client Player's Response to the given Message
        :param message: The Message
        :return: The Player's Response
        """
        return message.get_response(self.external_player)


class ProxyDealer(MessageSocket, IProxyDealer):
    """ A class representing a Proxy Dealer """

    def __init__(self,
                 held_socket:           socket.SocketType,
                 client_player:         ClientPlayer,
                 food_on_watering_hole: Natural = NO_FOOD_TOKENS) -> None:
        """ Construct a Proxy Dealer
        :param held_socket: The Socket this Proxy dealClientPlayer
        :param client_player: The Client Player
        """
        MessageSocket.__init__(self, held_socket)
        self._client_player = Unset              # type: ClientPlayer
        self._next_server_message_types = Unset  # type: List[type(ServerMessageToClient)]
        self._food_on_watering_hole = Unset      # type: Natural

        self.client_player = client_player
        self.send_sign_up()  # Sets self.next_server_message_types
        self.food_on_watering_hole = food_on_watering_hole

    def run_evolution_for_client(self) -> None:
        """ Run the game evolution for the Client """
        evo_print(START_MESSAGE)
        while True:
            evo_print("")
            message = InvalidMessage
            try:
                message = self.receive_message_to_client()
            except TimeoutDecoratorError:
                return

            if message == InvalidMessage:
                return

            message_to_client = cast(ServerMessageToClient, message)
            message_to_client.update(self)

            if message_to_client.has_response:
                response = self.get_clients_response(message_to_client)
                if response != ValidNoPlayerResponse:
                    self.send_message(response)

    def get_clients_response(self, message: ServerMessageToClient) -> PlayerResponse:
        """ Get the Client Player's Response to the given message
        :param message: The Server Message to Client
        :return: The Client Player's Response
        """
        return self.client_player.get_response(message)

    @timeout(CLIENT_MESSAGE_TIMEOUT)
    def receive_message_to_client(self) -> ServerMessageToClient:
        """ Receive the next Message to this Client
        Effect: Modifies the next server message types if valid
        :return: The Server Message to Client of Invalid Message
        """
        message = self.receive_message_of_types(self.next_server_message_types)
        if message != InvalidMessage:
            message_to_client = cast(ServerMessageToClient, message)
            self.next_server_message_types = message_to_client.next_server_message_types

        return message

    def send_sign_up(self) -> None:
        """ Send the Sign Up Message
        Effect: Modifies the next Server Message type accepted
        """
        sign_up = SignUpMessage(self.client_player_name)
        self.send_message(sign_up)
        self.next_server_message_types = [OkayMessageToClient]

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
        self.client_player.update(player_id, species_list, food_bag, hand)

    @property
    def client_player(self) -> ClientPlayer:
        """ Get the Client Player """
        return assert_set(self._client_player)

    @client_player.setter
    def client_player(self, client_player: ClientPlayer) -> None:
        """ Set the Client Player """
        assert_type(client_player, of_type=ClientPlayer, func_name="client_player")

        self._client_player = client_player

    @property
    def client_player_name(self) -> OptStr:
        """ Get the name of the Client Player """
        return self.client_player.player_name

    @property
    def next_server_message_types(self) -> List[type(ServerMessageToClient)]:
        """ Gets next Server Message Type"""
        return assert_set(self._next_server_message_types)

    @next_server_message_types.setter
    def next_server_message_types(self, next_server_message_types: List[type(ServerMessageToClient)]) -> None:
        """ Sets the next Server Message type"""
        assert_type(next_server_message_types, list, of_type=type(ServerMessageToClient),
                    func_name="next_server_message_types")

        self._next_server_message_types = next_server_message_types
