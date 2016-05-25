from evolution.messages.server_messages.all_server_message import *
from evolution.external_players.abs_external_player import *
from evolution.messages.player_messages.sign_up_message import *
from evolution.messages.message_socket import *


class ProxyPlayer(AbsExternalPlayer, MessageSocket):
    """ A class representing a Proxy Player which communicates with a Client """

    def __init__(self,
                 player_id:            PlayerId,
                 player_configuration: PlayerConfiguration,
                 held_socket:          socket.SocketType):
        """ Construct a ProxyPlayer with its corresponding PlayerState
        :param player_id: The id of the Player
        :param player_configuration: This Silly Player's state
        :param held_socket: The socket this Player communicates through
        """
        AbsExternalPlayer.__init__(self, player_id, player_configuration)
        MessageSocket.__init__(self, held_socket)

    def send_new_player(self) -> PlayerResponse:
        """ Send the New Player message to the Client
        Effect: Sends a message over the socket to the Client
        """
        new_player_msg = NewPlayerServerMessage(cast(PlayerId, self.player_id))
        self.send_message(new_player_msg)
        return ValidNoPlayerResponse

    def start_turn(self, food_on_watering_hole: Natural) -> PlayerResponse:
        """ Start the Turn by send the Player State
        Effect: Start the Turn by sending the external player this Player's state
        :param food_on_watering_hole: The food on the watering hole
        :return: No Response
        """
        message = StartTurnServerMessage.make_from_watering_hole_player_configuration(food_on_watering_hole,
                                                                                      self.player_configuration)
        self.send_message(message)
        return ValidNoPlayerResponse

    def choose_feeding(self,
                       num_tokens_on_watering_hole: Natural,
                       other_players:               List[PlayerConfiguration]) -> OptValidFeedingChoice:
        """ Send a Choose Feeding Message to a messages Player and Interpret the Response
        :param num_tokens_on_watering_hole: the number of tokens on the watering hole
        :param other_players: the states of the other players in the game
        :return: The Opt Valid Feeding Choice received from the wire
        """
        message = ChooseFeedingServerMessage.make_from_player_configs_and_watering_hole(self.player_configuration,
                                                                                        num_tokens_on_watering_hole,
                                                                                        other_players)
        return self.get_response_to_message(message, FeedingChoice)

    def choose_action(self,
                      before_players: List[PlayerConfiguration],
                      after_players:  List[PlayerConfiguration]) -> OptValidAction:
        """ Send a Choose Action Message to a messages Player and Interpret the Response
        :param before_players: The list of players whose turns preceded this player
        :param after_players: The list of players whose turns are after this player
        :return: Optional Valid Action received from the wire
        """
        message = ChooseActionServerMessage.make_from_player_configs(before_players, after_players)
        return self.get_response_to_message(message, Action)

    def shut_down(self) -> PlayerResponse:
        """ Shut down this External Player
        Effect: Closes the socket
        """
        self.close()
        return ValidNoPlayerResponse

    def receive_message_of_types(self, message_types: List[type(Message)]) -> OptMessage:
        """ Receive the Response from the wire
        :param message_types: The type of Message
        :return: The resulting Response
        """
        evo_print(self.from_client_str)
        return MessageSocket.receive_message_of_types(self, message_types)

    def send_message(self, message: Message) -> None:
        """ Send the given Message over the socket
        Effect: Sends the Message over the socket
        :param message: The message
        """
        evo_print(self.to_client_str)
        MessageSocket.send_message(self, message)

    @property
    def to_client_str(self):
        return "\t\tTo Client {}:".format(self.player_id)

    @property
    def from_client_str(self):
        return "\t\tFrom Client {}:".format(self.player_id)