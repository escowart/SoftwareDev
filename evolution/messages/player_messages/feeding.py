from evolution.messages.player_messages.data_feeding_choices import *
from evolution.messages.player_messages.player_response import *

class Feeding(object):
    """ Represents a Feeding where a SimplePlayer must choose one of its Species to feed
    """
    def __init__(self,
                 player:         IPlayer,
                 watering_hole:  NaturalPlus,
                 other_players:  List[IPlayer]) -> None:
        """ Construct a Feeding
        :param player: The Player who is feeding
        :param watering_hole: The number of tokens on the watering hole
        :param other_players: The other players in the Game
        """
        if not isinstance(player, IPlayer):
            raise SetValueError("player_state: Must be a PlayerState, got: {}".format(player))
        elif not is_natural_plus(watering_hole):
            raise SetValueError("watering_hole: Must be a NaturalPlus, got: {}".format(watering_hole))
        elif not is_list(other_players, of_type=IPlayer):
            raise SetValueError("other_player_states: Must be a List[PlayerState] , got: {}"
                                .format(other_players))

        self.player = player                # type: IPlayer
        self.watering_hole = watering_hole  # type: NaturalPlus
        self.other_players = other_players  # type: List[IPlayer]

    def get_player_with_id(self, player_id: NaturalPlus) -> IPlayer:
        """ Get the SimplePlayer of the given id in the other_players list
        :param player_id: The id of the SimplePlayer you are looking for
        :return: The id of the SimplePlayer
        """
        for player_state in self.other_players:
            if player.player_id == player_id:
                return player_state

        raise ValueError("get_target_player: No PlayerState with id: {} exists".format(player_id))

    def __repr__(self):
        return "Feeding({}, {}, {})".format(self.player, self.watering_hole, self.other_players)

    def __eq__(self, other):
        return isinstance(other, Feeding) and \
               self.player == cast(Feeding, other).player and \
               self.watering_hole == cast(Feeding, other).watering_hole and \
               self.other_players == cast(Feeding, other).other_players