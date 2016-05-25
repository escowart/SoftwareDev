from evolution.root_evo.collections.list import *
import collections


class StartIterationIndexClass(NoIndexClass):
    """ A Start Iteration Index """
    def __init__(self) -> None:
        NoIndexClass.__init__(self)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, StartIterationIndexClass)

StartIterationIndex = StartIterationIndexClass()
OptStartIterationIndex = Union[StartIterationIndexClass, Index]


class StopIterationIndexClass(NoIndexClass):
    """ A Stop Iteration Index """
    def __init__(self) -> None:
        NoIndexClass.__init__(self)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, StopIterationIndexClass)

StopIterationIndex = StopIterationIndexClass()
OptStopIterationIndex = Union[StopIterationIndexClass, Index]


class Iterator(Generic[Item], collections.Iterator, metaclass=ABCMeta):
    """ An Abstract Class Iterator which iterates over an IList[Elem] """

    def __init__(self, previous_index: OptStartIterationIndex) -> None:
        """ Construct a Iterator of the item list
        :param item_list: The item list
        :param previous_index: The previous index to be iterated over
        """
        self._previous_index = Unset  # type: OptStartIterationIndex

        self.previous_index = previous_index

    @property
    def next_index(self) -> OptStopIterationIndex:
        """ Get the next index in the Iterator, StopIterationIndex if their is no next index """
        if self.is_empty:
            return StopIterationIndex
        elif self.previous_index == StartIterationIndex:
            return DEFAULT_START_INDEX
        else:
            next_index = self.previous_index + 1

            if len(self) <= next_index:
                return StopIterationIndex
            else:
                return next_index

    @property
    def next_index_in_cycle(self) -> OptStopIterationIndex:
        """ Get the next index if this iterator cycles over its item list """
        if self.is_empty:
            return StartIterationIndex
        elif self.next_index == StopIterationIndex:
            return DEFAULT_START_INDEX
        else:
            return self.next_index

    def __len__(self) -> Natural:
        """ Get the length of this List[Item] """
        return len(self.item_list)

    @property
    def is_empty(self) -> bool:
        """ Is this Iterator empty? """
        return len(self.item_list) == EMPTY_LIST_LEN

    def __iter__(self) -> 'Iterator[Item]':
        """ Get the Iterator over this Iterator """
        return self

    def pop(self, item_index: Index) -> Item:
        """ Pop the item at the given index
        Effect: Pop the item at the index
        :param item_index: The index of the Item
        :return: The Item itself
        """
        self.item_list.pop(item_index)

    def remove(self, item: Item) -> None:
        """ Remove the item from the List
        :param item: The item
        """
        self.item_list.remove(item)

    def __getitem__(self, item_index: Index) -> Item:
        """ Get the item at the given index,
        :param item_index: The index of the item
        :return: The item at the given index
        """
        return self.item_list[item_index]

    def __setitem__(self, item_index: Index, new_item: Item):
        """ Set the item at the given index to the given new_item
        :param item_index: The index of the item
        :param new_item: The new Item value
        """
        self.item_list[item_index] = new_item

    def index(self, item: Item) -> Index:
        """ Get the index of the given item
        :param item: The item
        :return: The index of the item
        """
        return self.item_list.index(item)

    @property
    @abstractmethod
    def item_list(self) -> List[Item]:
        """ Get the List[Item] that is being iterated over """
        raise NotImplementedError("item_list")

    @property
    def previous_index(self) -> OptIndex:
        """ Get the previous value's index in the iteration """
        return assert_set(self._previous_index)

    @previous_index.setter
    def previous_index(self, last_index: Union[Index, StartIterationIndexClass]) -> None:
        """ Set the previous value's index in the iteration """
        if not is_index(last_index) and (last_index != StartIterationIndex):
            raise SetValueError("last_index: Must be Index or StartIterationIndex, got: {}".format(last_index))

        self._previous_index = last_index
