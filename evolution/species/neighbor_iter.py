from evolution.card_holders.all_card_holders import *


class SpeciesNeighborIterator(object):
    """ A class Species Neighbor Iterator which  """
    def __init__(self, species_list: List[ISpecies], next_index: Index = DEFAULT_START_INDEX) -> None:
        """ Construct a Species List Neighbor Iterator
        :param species_list:
        :param next_index:
        :return:
        """
        self._species_list = Unset
        self._next_index = Unset

        self.species_list = species_list
        self.next_index = next_index

    def __iter__(self):
        """ If ask for its iterator return self
        :return: self
        """
        return self

    def __next__(self) -> Tuple[OptSpecies, ISpecies, OptSpecies]:
        """ Get the next Species's right neighbor, the next Species, and next Species left neighbor
        :return: (left_neighbor, next_species, right_neighbor)
        """
        if self.next_index > self.final_index:
            raise StopIteration()

        left_neighbor = self.left_neighbor
        next_species = self.next_species
        right_neighbor = self.right_neighbor

        self._next_index += 1

        return left_neighbor, next_species, right_neighbor

    def __len__(self) -> Natural:
        """ Get the length of this """
        return len(self._species_list)

    @property
    def final_index(self) -> Natural:
        """ Get the final index, -1 for empty list """
        return len(self) - 1

    @property
    def species_list(self) -> Index:
        """ Get the Species List """
        if self._species_list == Unset:
            raise UnsetValueError("species_list: Not Yet Set")

        return self._species_list

    @species_list.setter
    def species_list(self, species_list: List[ISpecies]) -> None:
        """ Set the List[Species] """
        if not is_list(species_list, of_type=ISpecies):
            raise SetValueError("species_list: Must be an List[Species], got: {}".format(species_list))

        self._species_list = species_list

    @property
    def next_index(self) -> Index:
        """ Get the next Index """
        if self._next_index == Unset:
            raise UnsetValueError("next_index")

        return self._next_index

    @next_index.setter
    def next_index(self, next_index: Index) -> None:
        """ Set the next Index """
        if not is_index(next_index):
            raise SetValueError("next_index: Must be an Index, got: {}".format(next_index))

        self._next_index = next_index

    @property
    def left_neighbor(self) -> OptSpecies:
        """ Get the Left Neighbor of the next Species, None if the next Species is the first """
        if self.next_index <= 0:
            return NoSpecies

        return self.species_list[self.next_index - 1]

    @property
    def next_species(self) -> ISpecies:
        """ Get the Right Neighbor of the next Species, None if the next Species is the last """
        if 0 <= self.next_index <= self.final_index:
            return self.species_list[self.next_index]

        raise StopIteration("No more Species")

    @property
    def right_neighbor(self) -> OptSpecies:
        """ Get the Right Neighbor of the next Species, None if the next Species is the last """
        if self.next_index >= self.final_index:
            return NoSpecies

        return self.species_list[self.next_index + 1]
