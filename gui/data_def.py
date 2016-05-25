from gui.constants import *
import tkinter as tk
from typing import Optional

def dist(a: 'Posn', b: 'Posn') -> int:
    """ The Distance from Pos a to b
    :param a: Posn a
    :param b: Posn b
    :return: The Distance from a to b
    """
    return ((a.x - b.x)**2 + (a.y - b.y)**2) ^ (1/2)


def is_posn(value: Any) -> bool:
    """ Is the given value a Posn?
    :param value: The value being checked
    :return: True if the given value a Posn, False otherwise
    """
    return isinstance(value, tuple) and isinstance(value[0], int) and isinstance(value[1], int)

Posn = namedtuple("Posn", ['x', 'y'])


def sum_posn(posn_1: Posn, posn_2: Posn) -> Posn:
    """ Sum the two given Posns into a
    :param posn_1: 1st Posn
    :param posn_2: 2nd Posn
    :return: A new Posn which is the Sum of the Two Posn
    """
    return Posn(posn_1.x + posn_2.x, posn_1.y + posn_2.y)


def make_posn(old_posn: Posn = 'POSN_ORIGIN',
              x_offset: int=POSN_DEFAULT_X_OFFSET,
              y_offset: int=POSN_DEFAULT_Y_OFFSET) -> Posn:
    """ Make a new Posn at the given offset away from the given old_posn
    :param old_posn: The old Posn
    :param x_offset: The x offset
    :param y_offset: The y offset
    :return: The new Posn
    """
    return Posn(old_posn.x + x_offset, old_posn.y + y_offset)


POSN_ORIGIN = Posn(0, 0)
WATERING_HOLE_POSN = Posn(1, 1)

""" A 3-digit Hexadecimal Color """
HexColor = str

BLACK = "#000"     # type: HexColor
GREEN = "green"    # type: HexColor
YELLOW = "yellow"  # type: HexColor
WHITE = "white"    # type: HexColor
