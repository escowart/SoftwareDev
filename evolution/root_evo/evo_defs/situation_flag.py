import enum
from typing import Union, Any


OptSituationFlag = Union['SituationFlag', 'NoSituationFlagClass']


class NoSituationFlagClass(object):
    """ A class representing a No Situation Flag """
    def __repr__(self) -> str:
        return "NoSituationFlag"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, NoSituationFlagClass)

NoSituationFlag = NoSituationFlagClass()


class SituationFlag(enum.Enum):
    """ Enumeration of the possible relative owners of a TraitCard an attack scenario
    """
    ATTACKER = 1
    DEFENDER = 2
    DEFENDER_L_NEIGHBOR = 3
    DEFENDER_R_NEIGHBOR = 4

    @staticmethod
    def is_belligerent(flag: 'SituationFlag') -> bool:
        """ Is the given flag a belligerent?
        :param flag: Any Flag
        :return: True if flag is a belligerent, False otherwise
        """
        return flag is SituationFlag.ATTACKER or flag is SituationFlag.DEFENDER

    @staticmethod
    def is_defender(flag: 'SituationFlag'):
        """ Is the given flag an defender?
        :param flag: Any flag
        :return: True if flag is an defender, False otherwise
        """
        return flag is SituationFlag.DEFENDER

    @staticmethod
    def is_attacker(flag: 'SituationFlag'):
        """ Is the given flag an attacker?
        :param flag: Any flag
        :return: True if flag is an attacker, False otherwise
        """
        return flag is SituationFlag.ATTACKER

    @staticmethod
    def is_defender_neighbor(flag: 'SituationFlag') -> bool:
        """ Is the given flag a defender neighbor?
        :param flag: Any Flag
        :return: True if flag is a defender neighbor, False otherwise
        """
        return flag is SituationFlag.DEFENDER_L_NEIGHBOR or flag is SituationFlag.DEFENDER_R_NEIGHBOR

    @staticmethod
    def is_defender_left_neighbor(flag: 'SituationFlag') -> bool:
        """ Is the given flag a left defender neighbor?
        :param flag: Any Flag
        :return: True if flag is a left defender neighbor, False otherwise
        """
        return flag is SituationFlag.DEFENDER_L_NEIGHBOR

    @staticmethod
    def is_defender_right_neighbor(flag: 'SituationFlag') -> bool:
        """ Is the given flag a right defender neighbor?
        :param flag: Any Flag
        :return: True if flag is a right defender neighbor, False otherwise
        """
        return flag is SituationFlag.DEFENDER_R_NEIGHBOR
