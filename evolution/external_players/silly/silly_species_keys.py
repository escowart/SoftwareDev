from evolution.player.player import *


class SpeciesFeedType(enum.Enum):
    """ Represents the different types of feedings that can be picked,
    with their value representing the priority (higher number = higer priority)
    """
    STORE_FAT = 3
    FEEDABLE_VEG = 2
    FEEDABLE_CARN = 1
    FORGO_ATTACK = 0
    UNFEEDABLE = -1


@total_ordering
class SpeciesOrderedKey(OrderedKey[Species], metaclass=ABCMeta):
    """ A class representing a Species Ordered Key """
    def __init__(self, species: Species) -> None:
        """ Construct a Species Ordered Key from the given Species
        :param species: The Species
        """
        self._species = Unset  # type: Species

        self.species = species

    @property
    def species(self) -> Species:
        """ Get the Species """
        if self._species == Unset:
            raise UnsetValueError("species")

        return self._species

    @species.setter
    def species(self, species: Species) -> None:
        """ Get the Species """
        if not isinstance(species, Species):
            raise UnsetValueError("species: Must be a Species, got: {}".format(species))

        self._species = species


@total_ordering
class SimpleSpeciesOrderedKey(SpeciesOrderedKey):
    """ Representing a way of comparing Species according to the Simple Player specifications
    The Key Prioritizes Feed Type then for Store Foot then Prioritizes the fat food need
        Then Prioritizes by lexicographical by population, food already fed, and body size
    """

    def __init__(self, species: Species, owning_player: IPlayer, opponents: List[IPlayer]):
        """ Construct a Species Pick Key
        :param species: The Species
        :param owning_player: The PlayerState that owns the Species
        :param opponents: The Opponents' PlayerStates
        """
        SpeciesOrderedKey.__init__(self, species)
        self.opponents = opponents  # type: Player
        self.feed_type = get_species_feed_type(species, owning_player, opponents)  # type: 'SpeciesFeedType'

    def __gt__(self, other: 'SimpleSpeciesOrderedKey') -> bool:
        """ Checks if this SpeciesPickKey is greater than the given SpeciesPickKey
        :param other: The other SpeciesPickKey
        :return: True if this SpeciesPickKey is greater than the given SpeciesPickKey, False otherwise
        """
        if self.feed_type is not other.feed_type:
            return self.feed_type.value > other.feed_type.value
        if self.feed_type is SpeciesFeedType.STORE_FAT:
            return FatOrderKey(self.species) > FatOrderKey(other.species)
        if self.feed_type in (SpeciesFeedType.FEEDABLE_CARN, SpeciesFeedType.FEEDABLE_VEG):
            return species_order_key(self.species) > species_order_key(other.species)
        return False

    def __eq__(self, other: 'SimpleSpeciesOrderedKey') -> bool:
        """ Checks if this SpeciesPickKey is equal to the given SpeciesPickKey
        :param other: The other SpeciesPickKey
        :return: True if this SpeciesPickKey is equal to the given SpeciesPickKey, False otherwise
        """
        if not isinstance(other, SimpleSpeciesOrderedKey):
            return False
        if self.feed_type is not other.feed_type:
            return False
        # at this point we know both keys are the same
        if self.feed_type is SpeciesFeedType.STORE_FAT:
            return FatOrderKey(self.species) == FatOrderKey(other.species)
        if self.feed_type in (SpeciesFeedType.FEEDABLE_CARN, SpeciesFeedType.FEEDABLE_VEG):
            return species_order_key(self.species) == species_order_key(other.species)
        # both must be unfeedable
        return True


def get_species_feed_type(species: Species,
                          owning_player: IPlayer,
                          opponents: List[IPlayer]) -> SpeciesFeedType:
    """ Get the Species feed type of the given Species
    :param species: The Species
    :param owning_player: The PlayerState which owns the Species
    :param opponents: The Opponents' PlayerState
    :return: The corresponding SpeciesFeedType
    """
    if species.can_store_more_fat:
        return SpeciesFeedType.STORE_FAT
    elif species.is_hungry:
        if species.is_vegetarian:
            return SpeciesFeedType.FEEDABLE_VEG
        elif any(species.can_attack_player(opponent) for opponent in opponents):
            return SpeciesFeedType.FEEDABLE_CARN
        elif species.can_attack_player(owning_player):
            return SpeciesFeedType.FORGO_ATTACK

    return SpeciesFeedType.UNFEEDABLE


def species_order_key(species: Species) -> str:
    """ Convert the Species to a string/key which is the pop, num food tokens, body size
    :param species: The Species
    :return: The string/key
    """
    return str(species.population) + str(species.fed_food) + str(species.body_size)


@total_ordering
class FatOrderKey(SpeciesOrderedKey):
    """ A way of ordering a Fat Food need
    """

    def __init__(self, species: FatSpecies):
        """ Construct FatOrderKey
        :param species: The Species
        """
        SpeciesOrderedKey.__init__(self, species)

    def __gt__(self, other: 'FatOrderKey'):
        """ Is this FatOrderKey greater than the other FatOrderKey
        :param other: The other FatOrderKey
        :return: True if this FatOrderKey is greater than the other FatOrderKey, False otherwise
        """
        return (self.species.fat_tissue_need > other.species.fat_tissue_need or
                (self.species.fat_tissue_need == other.species.fat_tissue_need and
                 (species_order_key(self.species) > species_order_key(other.species))))

    def __eq__(self, other: 'FatOrderKey'):
        """ Is this FatOrderKey equal to the other FatOrderKey
        :param other: The other FatOrderKey
        :return: True if this FatOrderKey is equal to the other FatOrderKey, False otherwise
        """
        return self.species.fat_tissue_need == other.species.fat_tissue_need and \
               (species_order_key(self.species) == species_order_key(other.species))
