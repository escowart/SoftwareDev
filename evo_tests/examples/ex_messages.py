from evo_tests.examples.ex_species import *
from evo_tests.examples.ex_player import *
from evo_json.serializers.game_state import *


class ExampleMessages():

    def __init__(self):
        ex_players = ExamplePlayer()
        ex_species = ExampleSpecies()

        self.species_boards_norm = SpeciesBoards([ex_species.norm_default])
        self.species_boards_norm_serial = [[['food', 0], ['body', 0], ['population', 1], ['traits', []]]]

        self.player_state_norm = PlayerState.make_from_watering_hole_player_configuration(0,
                                                                                          ex_players.default.\
                                                                                          player_configuration)
        self.player_state_norm_serial = [0, 0, [], []]

        self.game_state_norm = GameState(0, [], [], 0, [])
        self.game_state_norm_serial = [0, [], [], 0, []]

