from gui.base_generators.complex_gen import *


class RowsIGen(ComplexIGen, StaticWidthGen, metaclass=ABCMeta):
    """ A class representing a Rows Image Generator which has a fixed width and a number of rows
    """

    def __init__(self,
                 width: Natural,
                 rows: OptList[GenAtPosn]=List,
                 has_border: bool = DEFAULT_HAS_BORDER) -> None:
        """ Construct a Rows Generator
        :param width: The width of the whole RowGenerator and all of its rows
        :param rows: The list of rows in the order they will be rendered
        """
        ComplexIGen.__init__(self, rows, has_border)
        StaticWidthGen.__init__(self, width)

    @property
    def current_height(self) -> Natural:
        """ Get the height of this """
        if self.num_rows == 0:
            return POSN_ORIGIN.y
        else:
            return self.last_row.posn.y + self.last_row.image_gen.height

    @property
    def rows(self) -> List[GenAtPosn]:
        """ Get the rows of this RowsIGen """
        return self.sub_gens

    @rows.setter
    def rows(self, rows: OptList[GenAtPosn]=NoList) -> None:
        """ Set the rows of this RowsIGen """
        self.sub_gens = rows

    @property
    def num_rows(self) -> Natural:
        """ Get the number of Rows """
        return len(self.rows)

    @property
    def last_row(self) -> GenAtPosn:
        """ Get the last row """
        return self.rows[-1]

    @property
    def next_posn(self) -> Posn:
        """ Get the next available position """
        return Posn(POSN_ORIGIN.x, self.current_height)

    def add_row(self, row: ImageGenerator) -> None:
        """ Add the given row to the end of this RowGenerator
        :param row: The row being added
        """
        if row.width != self.width:
            raise ValueError("add_row: All rows must have the same width")

        self.add_sub_gen(row, at_posn=self.next_posn)


class DynamicRowsIGen(RowsIGen, StaticHeightGen):
    """ A class representing a Rows Image Generator which has a fixed width and a number of rows
    """

    def __init__(self,
                 width: Natural,
                 rows: OptList[GenAtPosn]=NoList,
                 has_border: bool = DEFAULT_HAS_BORDER) -> None:
        """ Construct a Dynamic Rows IGen
        :param width: The width of the IGen
        :param rows: The rows of the IGen
        :param has_border: Does the IGen have a border
        """
        RowsIGen.__init__(self, width, rows, has_border)

    @property
    def height(self) -> Natural:
        """ Get the height of this Generator """
        return self.current_height


class RowSlotsIGen(RowsIGen, StaticHeightGen):
    """ A class representing a Slot Rows Image Generator which has a fixed number of Row slots and a fixed height
    """

    def __init__(self,
                 width: Natural,
                 height: Natural,
                 num_slots: Natural,
                 rows: OptList[GenAtPosn]=NoList,
                 has_border: bool = DEFAULT_HAS_BORDER) -> None:
        """ Construct a Rows Generator
        :param width: The width of the whole RowGenerator and all of its rows
        :param height: The height of the whole RowGenerator
        :param num_slots: The number of row slots in this generator
        :param rows: The list of rows in the order they will be rendered
        """
        RowsIGen.__init__(self, width, rows, has_border)
        StaticHeightGen.__init__(self, height)
        self._num_slots = None  # type: Natural

        self.num_slots = num_slots

    @property
    def num_slots(self) -> Natural:
        """ Get the number of slots in each Row """
        if self._num_slots is None:
            raise ValueError("row_height: Not Set")

        return self._num_slots

    @num_slots.setter
    def num_slots(self, num_slots: Natural) -> None:
        """ Set the number of slots in each Row """
        if not is_natural(num_slots):
            raise ValueError("num_slots: Must be Natural, got: {}".format(num_slots))

        self._num_slots = num_slots

    @property
    def remaining_slots(self) -> Natural:
        """ Get the number of remaining slots """
        return self.num_slots - self.num_rows

    @property
    def remaining_height(self) -> Natural:
        """ Get the total remaining height available for remaining slots """
        return self.height - self.current_height

    @property
    def remaining_slot_width(self) -> Natural:
        """ Get the width of each slot if all remaining slots have the same width """
        return int(self.remaining_height / self.remaining_slots)

    @property
    def all_slots_filled(self) -> bool:
        """ Are all the slots filled? """
        return self.num_rows >= self.num_slots

    def add_row(self, row: ImageGenerator) -> None:
        """ Add the given row to the end of this RowGenerator
        :param row: The row being added
        """
        if self.all_slots_filled:
            raise ValueError("add_row: All Slots have been filled cannot add")

        RowsIGen.add_row(self, row)