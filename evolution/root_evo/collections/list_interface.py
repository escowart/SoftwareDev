from evolution.root_evo.data_defs.key import *
from evolution.root_evo.data_defs.unset import *
import typing
CollectionType = Union[list, tuple, typing.Iterator, typing.Iterable]

OptCollectionType = Union[CollectionType, NoTypeClass]


class OptList(Generic[Item]):
    """ An OptList is one of:
        - NoList
        - List[Item]
    """


class NoListClass(OptList, NoValue):
    """ A No List class """

NoList = NoListClass()


class IList(OptList, metaclass=ABCMeta):
    """ An interface for List """

    @abstractmethod
    def __iter__(self):
        """ Get the Iterator over this List """
        raise NotImplementedError("__iter__")

    @abstractmethod
    def __len__(self) -> Natural:
        """ Get the length of this List """
        raise NotImplementedError("__len__")

    @abstractmethod
    def __getitem__(self, item_index: Index) -> Item:
        """ Get the Item at the index from this  List
        :param item_index: The index of the Item
        :return: The Item at the index
        """
        raise NotImplementedError("__getitem__")

    @abstractmethod
    def __setitem__(self, item_index: Index, new_item: Item) -> None:
        """ Get the Item at the index from this List
        Effect: Modifies the value at the given index to equal the given new Item
        :param item_index: The index of the Item
        :param new_item: The new item value
        """
        raise NotImplementedError("__setitem__")

    @abstractmethod
    def pop(self, item_index: Index) -> Item:
        """ Pop the Item at the given index
        Effect: Sets the value at the given index to RemovedItem
        :param item_index: The index of the Item
        :return: The Item itself
        """
        raise NotImplementedError("pop")

    @abstractmethod
    def remove(self, item: Item) -> None:
        """ Remove the item from the Removal List
        Effect: Sets the value at the index of the given item to RemovedItem
        :param item: The item
        """
        raise NotImplementedError("remove")
