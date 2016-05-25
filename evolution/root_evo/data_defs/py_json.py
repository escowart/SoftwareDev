from evolution.root_evo.data_defs.type_value import *

PyJSON = Union[bool, float, int, str, list, dict]


class InvalidPyJSONClass(NoValue):
    """ Invalid PyJSON class """

InvalidPyJSON = InvalidPyJSONClass()


OptPyJSON = Union[PyJSON, InvalidPyJSONClass]