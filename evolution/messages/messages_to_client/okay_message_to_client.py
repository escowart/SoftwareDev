from evolution.messages.messages_to_client.new_player_message_to_client import *


class OkayMessageToClient(OkayServerMessage, MessageToClient):
    """ A New Player Message To Client """

    def update(self, proxy_dealer: IProxyDealer) -> None:
        """ Update the Proxy dealers according to this Message to the Client
        Effect: Modifies the Proxy Dealer according to this Message
        :param proxy_dealer: The Proxy Dealer
        """
        pass

    @property
    def next_server_message_types(self) -> List[type(ServerMessageToClient)]:
        """ Get the Next Server Messages Types """
        return [NewPlayerMessageToClient]

    @property
    def has_response(self) -> bool:
        """ Does this Message have a Response? """
        return False

    def get_response(self, external_player: ExternalPlayer) -> PlayerResponse:
        """ Get the response to this Message
        :param external_player: The external player the response is received from
        :return: The Response to this Message
        """
        raise ValueError("{} has no response".format(name_of_class(self)))

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'OkayMessageToClient':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        return OkayMessageToClient()