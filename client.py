from evolution.dealers.proxy_dealer import *
from evolution.messages.messages_to_client.all_message_to_client import *


def run_evolution_client(player_name: OptStr = NoStr) -> None:
    """ Run the Evolution Client
    :param player_name: The name of the Player
    """
    proxy_dealer, client_socket = setup_client(player_name)
    proxy_dealer.run_evolution_for_client()
    client_socket.close()


def setup_client(player_name: OptStr = NoStr) -> Tuple[ProxyDealer, socket.SocketType]:
    """ Setup the Client and return the ProxyDealer and socket
    :param player_name: The name of the Player
    :return: The Proxy Dealer and Socket
    """
    client_socket = make_client_socket()
    client_player = ClientPlayer(external_player_type=SillyPlayer, player_name=player_name)
    proxy_dealer = ProxyDealer(client_socket, client_player)
    return proxy_dealer, client_socket


def make_client_socket() -> socket.SocketType:
    """ Make a Client Socket
    :return: The client socket
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((CLIENT_HOST_ADDRESS, CLIENT_PORT_ADDRESS))
    return client_socket
