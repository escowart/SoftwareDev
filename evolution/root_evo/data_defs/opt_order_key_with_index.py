from evolution.root_evo.collections.list import *

V = TypeVar('V')


class OptOrderedKeyWithIndex(Generic[V]):
    """ An OrderedKeyWithIndex is one of:
        - NoOrderedKeyWithIndex
        - OrderedKeyWithIndex[V]
    """

    def __init__(self, opt_key: OptOrderedKey, opt_index: OptIndex) -> None:
        """ Construct a OptOrderedKey With an Index
        :param opt_key: The ordered key
        :param opt_index: The index of the key in a list of objects
        """
        self._opt_key = Unset    # type: OptOrderedKey
        self._opt_index = Unset  # type: OptIndex

        self.opt_key = opt_key
        self.opt_index = opt_index

    @property
    def opt_key(self) -> OptOrderedKey:
        """ Get the key of this """
        return assert_set(self._opt_key)

    @opt_key.setter
    def opt_key(self, opt_key: OptOrderedKey) -> None:
        """ Get the key of this """
        assert_type(opt_key, of_type=(OptOrderedKey, str, int))
        self._opt_key = opt_key

    @property
    def key(self) -> OrderedKey:
        """ Get the key of this """
        if self.opt_index == NoOrderedKey:
            raise ValueError("opt_index: This Has NoOrderedKey")

        return cast(OrderedKey, self.opt_key)

    @key.setter
    def key(self, key: OrderedKey) -> None:
        """ Set the key of this """
        self.opt_key = key

    @property
    def opt_index(self) -> OptIndex:
        """ Get the index of this """
        if self._opt_index == Unset:
            raise UnsetValueError("opt_index")

        return self._opt_index

    @opt_index.setter
    def opt_index(self, opt_index: OptIndex) -> None:
        """ Get the OptIndex of this """
        if not is_opt_index(opt_index):
            raise ValueError("opt_index: Must be an OptIndex, got: {}".format(opt_index))

        self._opt_index = opt_index

    @property
    def index(self) -> Index:
        """ Get the index of this """
        if self.opt_index == NoIndex:
            raise ValueError("index: This Has NoIndex")

        return cast(Index, self.opt_index)

    @index.setter
    def index(self, index: Index) -> None:
        """ Set the index of this """
        self.opt_index = index


class NoOrderedKeyWithIndexClass(OptOrderedKeyWithIndex):
    """ A class representing a No-OrderedKeyWithIndex
        If either key or index is a No-Value then the OreredKeyWithIndex is a No-value
    """
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, OptOrderedKeyWithIndex):
            return False

        other_opt_okwi = cast(OptOrderedKeyWithIndex, other)
        return (other_opt_okwi.opt_index == NoIndex) or (other_opt_okwi.opt_key == NoOrderedKey)

NoOrderedKeyWithIndex = NoOrderedKeyWithIndexClass(NoOrderedKey, NoIndex)
