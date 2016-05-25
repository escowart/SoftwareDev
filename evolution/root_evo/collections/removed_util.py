from evolution.root_evo.collections.iterator import *


class RemovedItemClass(object):
    """ A class representing a Removed Item from a List """
    def __repr__(self) -> str:
        return "RemovedItem"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, RemovedItemClass)

RemovedItem = RemovedItemClass()


OptItem = Union['Item', 'RemovedItemClass']


class RemovedItemError(ValueError):
    """ A class representing a Removed Item Value Error """
    def __init__(self, *args, **kwargs) -> None:
        ValueError.__init__(self, *args, **kwargs)


class OptRemovalList(Generic[Item]):
    """ An OptRemovalList is one of:
        - NoRemovalList
        - RemovalList
    """


class NoRemovalListClass(OptRemovalList):
    """ A class representing a No-RemovalList """
    def __repr__(self) -> str:
        return "NoRemovalList"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, NoRemovalListClass)

NoRemovalList = NoRemovalListClass()


class IRemovalList(OptRemovalList, IList, metaclass=ABCMeta):
    """ An interface for a Removal List """
