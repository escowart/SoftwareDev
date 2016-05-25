from evolution.messages.messages_to_client.message_to_client import *


class StartTurnMessageToClient(StartTurnServerMessage, MessageToClient):
    """ A Start Turn Message To Client """

    def update(self, proxy_dealer: IProxyDealer) -> None:
        """ Update the Proxy dealers according to this Message to the Client
        Effect: Modifies the Proxy Dealer according to this Message
        :param proxy_dealer: The Proxy Dealer
        """
        proxy_dealer.update_client_player(species_list=self.species_list, food_bag=self.food_bag, hand=self.hand)

    @property
    def next_server_message_types(self) -> List[type(ServerMessageToClient)]:
        """ Get the Next Server Messages Types """
        return [ChooseActionMessageToClient]

    @property
    def has_response(self) -> bool:
        """ Does this Message have a Response? """
        return True

    def get_response(self, external_player: ExternalPlayer) -> PlayerResponse:
        """ Get the response to this Message
        :param external_player: The external player the response is received from
        :return: The Response to this Message
        """
        external_player.start_turn(self.food_on_watering_hole)
        return ValidNoPlayerResponse

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'StartTurnMessageToClient':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        message = PlayerState.deserialize(py_json)
        return StartTurnMessageToClient(message.food_on_watering_hole,
                                        message.food_bag,
                                        message.species_list,
                                        message.hand)


class ChooseActionMessageToClient(ChooseActionServerMessage, MessageToClient):
    """ A Choose Action Message To Client """

    def update(self, proxy_dealer: IProxyDealer) -> None:
        """ Update the Proxy dealers according to this Message to the Client
        Effect: Modifies the Proxy Dealer according to this Message
        :param proxy_dealer: The Proxy Dealer
        """
        pass

    @property
    def next_server_message_types(self) -> List[type(ServerMessageToClient)]:
        """ Get the Next Server Messages Types """
        return [StartTurnMessageToClient, ChooseFeedingMessageToClient]

    @property
    def has_response(self) -> bool:
        """ Does this Message have a Response? """
        return True

    def get_response(self, external_player: ExternalPlayer) -> PlayerResponse:
        """ Get the response to this Message
        :param external_player: The external player the response is received from
        :return: The Response to this Message
        """
        return external_player.choose_action(self.before_player_configs, self.after_player_configs)

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'ChooseActionMessageToClient':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        message = ChooseActionServerMessage.deserialize(py_json)
        return ChooseActionMessageToClient(message.before_boards, message.after_boards)


class ChooseFeedingMessageToClient(ChooseFeedingServerMessage, MessageToClient):
    """ A Choose Feeding Message To Client """

    def update(self, proxy_dealer: IProxyDealer) -> None:
        """ Update the Proxy dealers according to this Message to the Client
        Effect: Modifies the Proxy Dealer according to this Message
        :param proxy_dealer: The Proxy Dealer
        """
        proxy_dealer.update_client_player(species_list=self.species_list, food_bag=self.food_bag, hand=self.hand)

    @property
    def next_server_message_types(self) -> List[type(ServerMessageToClient)]:
        """ Get the Next Server Messages Types """
        return [StartTurnMessageToClient, ChooseFeedingMessageToClient]

    @property
    def has_response(self) -> bool:
        """ Does this Message have a Response? """
        return True

    def get_response(self, external_player: ExternalPlayer) -> PlayerResponse:
        """ Get the response to this Message
        :param external_player: The external player the response is received from
        :return: The Response to this Message
        """
        return external_player.choose_feeding(self.food_on_watering_hole, self.other_player_configs)

    @staticmethod
    def deserialize(py_json: PyJSON) -> 'ChooseFeedingMessageToClient':
        """ Deserialize the given value into a instance of this Serializer?
        :param py_json: A PyJSON value
        :return: An instance of this Deserialized
        """
        message = ChooseFeedingServerMessage.deserialize(py_json)
        return ChooseFeedingMessageToClient(message.food_bag,
                                            message.species_list,
                                            message.hand,
                                            message.food_on_watering_hole,
                                            message.other_player_boards)