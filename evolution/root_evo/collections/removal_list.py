from evolution.root_evo.collections.removed_util import *


class RemovalList(IRemovalList):
    """ A class representing a Removal List:
        When a value is removed it is replaced with a RemovedItem value.
        Whenever a RemovedItem is access, a RemovedItemError is raised
        """

    def __init__(self, item_list: List[Item]) -> None:
        self._item_list = Unset  # type: List[OptItem]

        self.item_list = item_list

    def __iter__(self) -> Iterator[Item]:
        """ Get the Iterator over this Iterator """
        return iter(self.item_list)

    def __len__(self) -> Natural:
        """ Get the length of this Removal List """
        return len(self.item_list)

    def pop(self, item_index: Index) -> Item:
        """ Pop the Item at the given index and Replace it with a RemovedItem
        Effect: Sets the value at the given index to RemovedItem
        :param item_index: The index of the Item
        :return: The Item itself
        """
        item = self[item_index]
        self[item_index] = RemovedItem
        return item

    def remove(self, item: Item) -> None:
        """ Remove the item from the Removal List
        Effect: Sets the value at the index of the given item to RemovedItem
        :param item: The item
        """
        item_index = self.index(item)
        self.pop(item_index)

    @property
    def clean_list(self) -> List[Item]:
        """ Get the clean version of this Removal List with no RemovedItems """
        return [item for item in self.item_list if item != RemovedItem]

    def has_unremoved_item_at_index(self, index: Index) -> bool:
        """ Does this Removal List have an unremoved item at the given index?
        :param index: The index in question
        :return: True if there is a non-RemovedItem at the given index, False otherwise
        """
        return is_index(index) and (index < len(self)) and (self[index] != RemovedItem)

    def __getitem__(self, item_index: Index) -> Item:
        """ Get the item at the given index, raises RemovedItemError if the Item was already removed
        :param item_index: The index of the item
        :return: The item at the given index
        :raises: RemovedItemError if the Item was already removed
        """
        item = self.item_list[item_index]

        if item == RemovedItem:
            raise RemovedItemError("__getitem__")
        else:
            return item

    def __setitem__(self, item_index: Index, new_item: OptItem):
        """ Set the item at the given index to the given new_item
        :param item_index: The index of the item
        :param new_item: The new Item value
        """
        self.item_list[item_index] = new_item

    def index(self, item: Item, start_range: Index = NoIndex, end_range: Index = NoIndex) -> Index:
        """ Get the index of the given item
        :param item: The item
        :param start_range: The start of the range the item is being search for in
        :param end_range: The end of the range the item is being search for in
        :return: The index of the item
        """
        return self.item_list.index(item,
                                    None if start_range == NoIndex else start_range,
                                    None if end_range == NoIndex else end_range)

    @property
    def item_list(self) -> List[OptItem]:
        """ Get the list value """
        return assert_set(self._item_list)

    @item_list.setter
    def item_list(self, item_list: List[OptItem]) -> None:
        """ Set the list value """
        assert_type(item_list, list)
        self._item_list = item_list

    def __repr__(self) -> str:
        return "RemovalList({})".format(self.item_list)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, RemovalList) and (self.item_list == cast(RemovalList, other).item_list)

    class RemovalIterator(Iterator[Item]):
        """ An Iterator for iterating over a removal list and cleaning it upon completion of iteration """

        def __init__(self, removal_list: 'RemovalList[Item]', previous_index: OptIndex = StartIterationIndex) -> None:
            """ Construct a Removal Iterator with a removal list
            :param removal_list: The Removal List
            :param previous_index: The previous
            """
            Iterator.__init__(self, removal_list, previous_index)

        def __next__(self) -> Item:
            """ Get the next Item in this Iterator, Clean upon completion
            Effect: Modifies previous index to be the next index Cleans upon completion of Iteration
            :return: The next Item
            """
            if self.next_index == StopIterationIndex:
                raise StopIteration()
            else:
                next_value = self.removal_list[self.next_index]
                self.previous_index = self.next_index
                return next_value

        @property
        def clean_list(self) -> List[Item]:
            """ Get the clean version of this Removal List with no RemovedItems """
            return self.removal_list.clean_list

        @property
        def removal_list(self) -> 'RemovalList[Item]':
            """ Get the removal list """
            return self.item_list

        @removal_list.setter
        def removal_list(self, removal_list: 'RemovalList[Item]') -> None:
            """ Set the removal list """
            self.item_list = removal_list

        def __repr__(self) -> str:
            return "RemovalIterator[Elem]({})".format(self.removal_list)


def rem_list(item_list: List[Item]) -> RemovalList[Item]:
    """ Construct a Removal List of Items
    :param item_list: The item Iterator being used in the Removal List
    :return: The Removal List of Items
    """
    return RemovalList(item_list)

