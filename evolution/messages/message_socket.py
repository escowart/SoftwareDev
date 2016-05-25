import socket
import json
from evolution.messages.message import *


class MessageSocket(object):
    """ A class representing an object which holds a socket """

    def __init__(self, held_socket: socket.SocketType, collected_data: OptStr = NoStr) -> None:
        """ Construct a message Socket
        :param held_socket: The socket being held
        :param collected_data: The collected data
        """
        self._held_socket = Unset     # type: socket.SocketType
        self._collected_data = Unset  # type: str

        self.held_socket = held_socket
        self.collected_data = collected_data

    def get_response_to_message(self,
                                message:       Message,
                                response_type: type(Response)) -> OptResponse:
        """ Get the response to the given message Serializer and deserialize the response
        :param message: The message
        :param response_type: tHe response deserializer type
        :return: Either the deserialized response or return invalid response
        """
        self.send_message(message)
        return self.receive_message(response_type)

    def send(self, py_json: PyJSON) -> None:
        """ Send the given PyJSON over the socket
        Effect: Sends the given value over the socket to be received
        :param py_json: The PyJSON
        """
        json_str = json.dumps(py_json)
        self.held_socket.sendall(json_str.encode())

    def send_message(self, message: Message) -> None:
        """ Send the given Message over the socket
        Effect: Sends the Message over the socket
        :param message: The message
        """
        evo_print("\t\t\tSend Message: {}".format(message))
        pj_message = message.serialize()
        self.send(pj_message)

    def receive(self) -> PyJSON:
        """ Receives on the socket and wait for response and return it
        Effect: Receives from the wire
        """
        json_data = self.held_socket.recv(PACKET_SIZE)
        self.collected_data += json_data.decode()
        py_json = self.next_py_json()
        return py_json

    def receive_message(self, message_type: type(Message)) -> OptMessage:
        """ Receive the Response from the wire
        :param message_type: The type of Message
        :return: The resulting Response
        """
        message_types = cast(List[type(Message)], [message_type])
        return self.receive_message_of_types(message_types)

    def receive_message_of_types(self, message_types: List[type(Message)]) -> OptMessage:
        """ Receive the Response from the wire
        :param message_types: The type of Message
        :return: The resulting Response
        """
        py_json = self.receive()
        for message_type in message_types:
            if message_type.can_deserialize(py_json):
                message = message_type.deserialize(py_json)
                evo_print("\t\t\tReceived Message: {}".format(message))
                return message

        return InvalidMessage

    def close(self) -> None:
        """ Close the Socket
        Effect: Close the Socket
        """
        self.held_socket.close()

    def next_py_json(self) -> OptPyJSON:
        """ Get the next PyJSON from the collected data
        Effect: Modifies the collected data to remove the returned value
        :return: The next PyJSON
        """
        total_len = len(self.collected_data)
        for index in range(total_len):
            try:
                len_data = index + 1
                coll_data = self.collected_data[:len_data]
                py_json = json.loads(coll_data)

                rest_data = ""
                if len_data < total_len:
                    rest_data = self.collected_data[len_data:]

                self.collected_data = rest_data
                return py_json
            except json.decoder.JSONDecodeError:
                pass
        return InvalidPyJSON

    @property
    def held_socket(self) -> socket.SocketType:
        """ Get the held socket """
        return assert_set(self._held_socket)

    @held_socket.setter
    def held_socket(self, held_socket: socket.SocketType) -> None:
        """ Set the held socket """
        assert_type(held_socket, of_type=socket.SocketType, func_name="held_socket")
        self._held_socket = held_socket

    @property
    def collected_data(self) -> str:
        """ Get the Collected Data """
        return assert_set(self._collected_data)

    @collected_data.setter
    def collected_data(self, collected_data: OptStr) -> None:
        """ Set the held socket """
        if collected_data == NoStr:
            collected_data = ""

        assert_type(collected_data, of_type=str, func_name="collected_data")
        self._collected_data = collected_data

