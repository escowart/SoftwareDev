import json
import sys
import socket

from evolution.dealers.dealer import Dealer
from evo_json.all_converters import *


def run_evolution_server() -> None:
    """ Main function for running the Evolution Game
    Effect: Runs the Game Evolution
    """
    dealer, server_socket = setup_server()

    if dealer != NoDealer:
        cast(Dealer, dealer).run_evolution()

    if server_socket != INVALID_SOCKET:
        server_socket.close()


def setup_server() -> Tuple[OptDealer, socket.SocketType]:
    """ Setup the Server and return the Dealer and socket
    :return: The new Dealer and Socket
    """
    dealer = NoDealer
    server_socket = make_server_socket()

    if server_socket == INVALID_SOCKET:
        print("\nInvalid Server Socket\n")
    else:
        print("\nWaiting on Players to Connect ...\n")
        players = make_players(server_socket)
        num_players = len(players)
        if num_players < MIN_NUM_PLAYERS:
            print("\nNot Enough players in the Game to Start, need: {}, got: {}\n".format(MIN_NUM_PLAYERS, num_players))
        else:
            dealer = Dealer.make_evolution_dealer(players)

    return dealer, server_socket


def make_server_socket() -> socket.SocketType:
    """ Make the socket for the whole server
    :return: The socket for the server
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST_ADDRESS, SERVER_PORT_ADDRESS))
    server_socket.listen(MAX_NUM_PLAYERS)
    return server_socket


def make_players(server_socket: socket.SocketType) -> List[Player]:
    """ Create the Players of the game by opening sockets for clients to connect to
    :param server_socket: The main socket of the Server which the Remote Player sockets will generate off of
    :return: The Players in the game
    """
    players = []
    player_id = START_PLAYER_ID

    while len(players) < MAX_NUM_PLAYERS:
        try:
            client_socket, address = accept_from_socket(server_socket)
            if client_socket == INVALID_SOCKET:
                break
        except TimeoutDecoratorError:
            break

        player_id = add_new_player(players, player_id, client_socket)

    return players


@timeout(START_CONNECTION_TIMEOUT)
def accept_from_socket(server_socket: socket.SocketType) -> Tuple[socket.SocketType, str]:
    """ Accept from the sever socket a client socket
    :param server_socket: The Server's Socket
    :return: The client socket and the address of the client
    """
    return server_socket.accept()


def add_new_player(players: List[Player], player_id: PlayerId, client_socket: socket.SocketType) -> PlayerId:
    """ Add a new Player with an External Proxy Player
    Effect: Appends a new Player on the Players list
    :param players: The Players so far
    :param player_id: The last Player's ID
    :param client_socket: The client's socket
    :return: The next Players id
    """
    success, player_name = set_up_proxy(client_socket)
    if not success:
        print("Couldn't Setup Proxy for Player")
        return player_id

    player = make_player(player_id, client_socket, player_name)
    if player == InvalidPlayer:
        return player_id

    players.append(player)
    return player_id + 1


def make_player(player_id: PlayerId, client_socket: socket.SocketType, player_name: OptStr = NoStr) -> OptPlayer:
    """ Make a new Player with an External Proxy Player
    :param player_id: The last Player's ID
    :param client_socket: The Client's Socket
    :param player_name: The name of the Player
    """
    player = Player(player_id)
    proxy_player = ProxyPlayer(player.player_id, player.player_configuration, client_socket)
    player.external_player = proxy_player
    player.player_name = player_name

    if player.send_new_player():
        print("Player {} has connected".format(player_id))
        return player
    else:
        return InvalidPlayer


def set_up_proxy(held_socket: socket.SocketType) -> Tuple[bool, OptStr]:
    """ Receive a Sign-Up Message from the client and respond with a New Player Message
    :return: The True and name of the Player if successful, False and NoStr otherwise
    """
    socket_holder = MessageSocket(held_socket)
    try:
        sign_up = cast(SignUpMessage, socket_holder.receive_message(SignUpMessage))
        okay = OkayServerMessage()
        if (sign_up == InvalidMessage) or (socket_holder.send_message(okay) == InvalidMessage):
            return (False, NoStr)
        else:
            return (True, sign_up.info)
    except Exception:
        return (False, NoStr)


if __name__ == "__main__":
    run_evolution_server()
