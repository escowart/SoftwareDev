from gui.base_generators.complex_gen import *


class ColumnsIGen(ComplexIGen, StaticHeightGen, metaclass=ABCMeta):
    """ A class representing a columns Image Generator which has a fixed width and a number of rows
    """

    def __init__(self,
                 height: Natural,
                 columns: OptList[GenAtPosn]=NoList,
                 has_border: bool = DEFAULT_HAS_BORDER) -> None:
        """ Construct a Columns Generator
        :param height: The height of the whole Columns Generator and all of its rows
        :param columns: The list of columns in the order they will be rendered
        """
        ComplexIGen.__init__(self, columns, has_border)
        StaticHeightGen.__init__(self, height)

    @property
    def current_width(self) -> Natural:
        """ Get the current width of this whole object """
        if self.num_columns == 0:
            return POSN_ORIGIN.x
        else:
            return self.last_column.posn.x + self.last_column.image_gen.width

    @property
    def columns(self) -> List[GenAtPosn]:
        """ Get the columns of this ColumnsIGen """
        return self.sub_gens

    @columns.setter
    def columns(self, rows: OptList[GenAtPosn] = NoList) -> None:
        """ Set the columns of this ColumnsIGen """
        self.sub_gens = rows

    @property
    def num_columns(self) -> Natural:
        """ Get the number of columns """
        return len(self.columns)

    @property
    def last_column(self) -> GenAtPosn:
        """ Get the last column """
        return self.columns[-1]

    @property
    def next_posn(self) -> Posn:
        """ Get the next available position """
        return Posn(self.current_width, POSN_ORIGIN.y)

    def add_column(self, column: ImageGenerator) -> None:
        """ Add the given column to the end of this RowGenerator
        :param column: The column being added
        """
        # if column.height != self.height:
        #    raise ValueError("add_column: All columns must have the same height")

        self.add_sub_gen(column, at_posn=self.next_posn)


class DynamicColumnsIGen(ColumnsIGen):
    """ A class representing a Dynamic Columns IGen which can have columns of any width
    """
    def __init__(self,
                 height: Natural,
                 columns: OptList[GenAtPosn]=NoList,
                 has_border: bool = DEFAULT_HAS_BORDER) -> None:
        """ Construct a DynamicColumnsIGen
        :param height: The height of the Image
        :param columns: The columns of the IGen
        :param has_border: Does the Image have a Border
        """
        ColumnsIGen.__init__(self, height, columns, has_border)

    @property
    def width(self) -> Natural:
        """ Get the height of this """
        return self.current_width


class ColumnSlotsGenerator(ColumnsIGen, StaticWidthGen):
    """ A class representing a Slot Rows Image Generator which has a fixed number of Row slots and a fixed height
    """

    def __init__(self,
                 width: Natural,
                 height: Natural,
                 num_slots: Natural,
                 columns: OptList[GenAtPosn]=NoList,
                 has_border: bool = DEFAULT_HAS_BORDER) -> None:
        """ Construct a Rows Generator
        :param width: The width of the whole Generator
        :param height: The height of the whole ColumnsIGen and all of its columns
        :param num_slots: The number of row slots in this generator
        :param columns: The list of columns in the order they will be rendered
        """
        ColumnsIGen.__init__(self, height, columns, has_border)
        StaticWidthGen.__init__(self, width)
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
        return self.num_slots - self.num_columns

    @property
    def remaining_width(self) -> Natural:
        """ Get the total remaining width available for remaining slots """
        return self.width - self.current_width

    @property
    def remaining_slot_width(self) -> Natural:
        """ Get the width of each slot if all remaining slots have the same width """
        return int(self.remaining_width / self.remaining_slots)

    @property
    def all_slots_filled(self) -> bool:
        """ Are all the slots filled? """
        return self.num_columns >= self.num_slots

    def add_column(self, column: ImageGenerator) -> None:
        """ Add the given column to the end of this Column Generator
        :param column: The column being added
        """
        if self.all_slots_filled:
            raise ValueError("add_column: All Slots have been filled cannot add")

        ColumnsIGen.add_column(self, column)

