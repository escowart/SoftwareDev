from evolution.player.player_interface import *


class OptPlayerSequence(object, metaclass=ABCMeta):
    """ An OptPlayerSequence is one of:
        - PlayerSequence
        - NoPlayerSequence
    """


class NoPlayerSequenceClass(OptPlayerSequence):
    """ The No-PlayerSequence """
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, NoPlayerSequenceClass)

NoPlayerSequence = NoPlayerSequenceClass()


class IPlayerSequence(OptPlayerSequence):
    """ An interface for PlayerSequence """

    def configuration_sequence_without(self, player: IPlayer) -> List[PlayerConfiguration]:
        """ Get this Sequence without the given Player as a List of Player Configurations
        :param player: The Player being removed
        :return: The Player Configuration Sequence without the given player
        """
        raise NO
