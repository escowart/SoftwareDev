import client
import server
import threading
import time
from evolution.all_evo import *


def run_server_with_clients() -> None:
    """ Run the Server with a Number of Clients with the Clients on separate threads
    Effect: Runs the Server on this Thread and creates a number of Threads each running a Client
    """
    input_str = input("Enter Number of Players: ")
    if not input_str.isdigit():
        print("Cannot Start Server with input: {}".format(input_str))
        return

    num_of_clients = int(input_str)

    try:
        client_threads = make_client_threads(num_of_clients)
    except ValueError as e:
        print("{}".format(e))
        return

    start_threads(client_threads)
    server.run_evolution_server()
    join_threads(client_threads, CLIENT_THREAD_TIMEOUT)


def make_client_threads(num_of_clients: int) -> List['ClientThread']:
    """ Make the given number of client threads
    :param num_of_clients: The number of threads
    :return: The Client Threads
    """
    assert_type(num_of_clients, of_type=Natural, func_name="num_of_clients")
    if MAX_NUM_CLIENT_THREADS <= num_of_clients:
        raise ValueError("make_client_thread: Given {}, must be less than {}".format(num_of_clients,
                                                                                     MAX_NUM_CLIENT_THREADS))

    return [ClientThread(i + 1) for i in range(num_of_clients)]


class ClientThread(threading.Thread):
    """ A Client Thread for running a client """
    def __init__(self, client_number: int) -> None:
        """ Construct a Client Thread """
        threading.Thread.__init__(self)
        self.client_number = client_number

    def run(self) -> None:
        """ Run this Client Thread by executing a Client
        Effect: Runs a single Client on this Thread
        """
        sleep_time = max(START_CONNECTION_TIMEOUT - 1, 1)
        time.sleep(sleep_time)
        client.run_evolution_client("{}".format(self))

    def __repr__(self) -> str:
        return "{}({})".format(name_of_class(self), self.client_number)


def start_threads(threads: List[threading.Thread]) -> None:
    """ Start the given threads
    Effect: Runs the threads
    :param threads: The threads
    """
    [thread.start() for thread in threads]


def join_threads(threads: List[threading.Thread], timeout: Natural=None) -> None:
    """ Join the given threads with the given timeout
    Effect: Join the threads
    :param threads: The threads
    :param timeout: The timeout of the threads
    """
    [thread.join(timeout) for thread in threads]


if __name__ == "__main__":
    run_server_with_clients()
