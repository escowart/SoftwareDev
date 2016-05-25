from gui.base_generators.columns_gens import *
from gui.base_generators.rows_gens import *


class GridIGen(DynamicRowsIGen):
    """ A class representing a Grid IGen which is a Dynamic Rows IGen of Column Slots IGens which wraps around when
    adding a new item into a slot.
    """

    def __init__(self,
                 width: Natural,
                 row_height: Natural,
                 num_slots_per_row: Natural,
                 rows: OptList[GenAtPosn]=NoList,
                 has_border: bool = DEFAULT_HAS_BORDER) -> None:
        """ Construct a Grid IGen
        :param width: The width of the IGen
        :param row_height: The height of each row
        :param num_slots_per_row: THe number of slots per row
        :param rows: The rows themselves
        :param has_border: Does it have a border
        """
        RowsIGen.__init__(self, width, rows, has_border)
        self._num_slots_per_row = None  # type: Natural
        self._row_height = None  # type: Natural

        self.num_slots_per_row = num_slots_per_row
        self.row_height = row_height

    @property
    def num_slots_per_row(self) -> Natural:
        """ Get the number of slots per row """
        if self._num_slots_per_row is None:
            raise ValueError("num_slots_per_row: Not Set")

        return self._num_slots_per_row

    @num_slots_per_row.setter
    def num_slots_per_row(self, num_slots_per_row: Natural) -> None:
        """ Set the number of slots per row """
        if not is_natural(num_slots_per_row):
            raise ValueError("num_slots_per_row: Must be Natural, got: {}".format(num_slots_per_row))

        self._num_slots_per_row = num_slots_per_row

    @property
    def row_height(self) -> Natural:
        """ Get the height of each row """
        if self._row_height is None:
            raise ValueError("row_height: Not Set")

        return self._row_height

    @row_height.setter
    def row_height(self, row_height: Natural) -> None:
        """ Set the height of each row """
        if not is_natural(row_height):
            raise ValueError("row_height: Must be Natural, got: {}".format(row_height))

        self._row_height = row_height

    @property
    def last_column_slots_gen(self) -> ColumnSlotsGenerator:
        """ Ge the last ColumnSlotsGenerator """
        return self.last_row.image_gen

    @property
    def last_row_filled(self) -> bool:
        """ Is the last row filled? """
        return (self.num_rows == 0) or self.last_column_slots_gen.all_slots_filled

    def add_to_next_column_slot(self, gen: ImageGenerator) -> None:
        """ Add the given Image Generator to the next sloumn slot
        :param gen: The generator
        """
        if self.last_row_filled:
            new_row = ColumnSlotsGenerator(width=self.width, height=self.row_height, num_slots=self.num_slots_per_row)
            self.add_row(new_row)

        self.last_column_slots_gen.add_column(gen)


class GridSlotsIGen(ComplexIGen):
    """ A class representing a Grid Slots IGen which has grid position (0,0) to (num_rows, num_columns) which draws
    each of the slots with the maximum width and height of each of them
    """

    def __init__(self, num_rows: Natural, num_columns: Natural) -> None:
        """ Construct a Grid Slots IGen
        :param num_rows: The number of rows
        :param num_columns: The number of columns
        """
        ComplexIGen.__init__(self, has_border=True)
        self._num_rows = None     # type: Natural
        self._num_columns = None  # type: Natural

        self.num_rows = num_rows
        self.num_columns = num_columns

    @property
    def num_rows(self) -> Natural:
        """ Get the number of rows """
        if self._num_rows is None:
            raise ValueError("num_rows: Not Set")

        return self._num_rows

    @num_rows.setter
    def num_rows(self, num_rows: Natural) -> None:
        """ Set the number of rows """
        if not is_natural(num_rows):
            raise ValueError("num_rows: Must be Natural, got: {}".format(num_rows))

        self._num_rows = num_rows

    @property
    def num_columns(self) -> Natural:
        """ Get the number of columns """
        if self._num_columns is None:
            raise ValueError("num_columns: Not Set")

        return self._num_columns

    @num_columns.setter
    def num_columns(self, num_columns: Natural) -> None:
        """ Set the number of columns """
        if not is_natural(num_columns):
            raise ValueError("num_columns: Must be Natural, got: {}".format(num_columns))

        self._num_columns = num_columns

    @property
    def max_slot_width(self) -> Natural:
        """ Get the width of each slot"""
        return max([sub_gen.image_gen.width for sub_gen in self.sub_gens], default=0)

    @property
    def max_slot_height(self) -> Natural:
        """ Get the width of each slot"""
        return max([sub_gen.image_gen.height for sub_gen in self.sub_gens], default=0)

    @property
    def width(self) -> Natural:
        """ Get the width of this IGen """
        return self.num_columns * self.max_slot_width

    @property
    def height(self) -> Natural:
        """ Get the height of this IGen """
        return self.num_rows * self.max_slot_height

    def place_at(self, igen: ImageGenerator, posn: Posn) -> None:
        """ Place the given IGen at the given position on the Grid
        :param igen: The IGen
        :param posn: The Position
        """
        self.add_sub_gen(igen, posn)

    def displays_at(self, canvas: tk.Canvas, posn: Posn) -> None:
        """ Display the Image at the given Position on the Canvas
        :param canvas: The Canvas the image will be drawn on
        :param posn: The position the image will be drawn
        """
        if self.has_border:
            border_rect = RectangleIGen(self.width, self.height, outline=BLACK, border_width=DEFAULT_OUTLINE_WIDTH)
            border_rect.displays_at(canvas, posn)

        for sub_gen in self.sub_gens:
            adjusted_posn = Posn(sub_gen.posn.x * self.max_slot_width, sub_gen.posn.y * self.max_slot_height)
            sub_gen.image_gen.displays_at(canvas, sum_posn(adjusted_posn, posn))



