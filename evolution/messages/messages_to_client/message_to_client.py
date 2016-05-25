from evolution.dealers.proxy_dealer_interface import *


class MessageToClient(metaclass=ABCMeta):
    """ A Message to a Client """

    @abstractmethod
    def update(self, proxy_dealer: IProxyDealer) -> None:
        """ Update the Proxy dealers according to this Message to the Client
        Effect: Modifies the Proxy Dealer according to this Message
        :param proxy_dealer: The Proxy Dealer
        """
        raise NotImplementedError("update")

    @property
    @abstractmethod
    def next_server_message_types(self) -> List[type('ServerMessageToClient')]:
        """ Get the Next Server Messages Types """
        raise NotImplementedError("next_server_message_types")

    @property
    @abstractmethod
    def has_response(self) -> bool:
        """ Does this Message have a Response? """
        raise NotImplementedError("has_response")

    @abstractmethod
    def get_response(self, external_player: ExternalPlayer) -> PlayerResponse:
        """ Get the response to this Message
        :param external_player: The external player the response is received from
        :return: The Response to this Message
        """
        raise NotImplementedError("get_response")


class ServerMessageToClient(Message, MessageToClient, metaclass=ABCMeta):
    """ A Server Message To Client is one of:
        - NewPlayerMessageToClient
        - OkayMessageToClient
        - StartTurnMessageToClient
        - ChooseActionMessageToClient
        - ChooseFeedingMessageToClient
    """

    @staticmethod
    def is_instance(self, value: Any) -> bool:
        return is_instance(value, Message) and is_instance(value, MessageToClient)










