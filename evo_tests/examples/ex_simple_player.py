from evo_tests.examples.ex_player import *


class ExampleSillyPlayers:
    def __init__(self):
        self.ex_players = ExamplePlayer()

        self.default = SillyPlayer(self.ex_players.default.player_configuration.player_id,
                                   self.ex_players.default.player_configuration)
        self.burr_veg = SillyPlayer(self.ex_players.burr_veg.player_configuration.player_id,
                                    self.ex_players.burr_veg.player_configuration)
        self.carn = SillyPlayer(self.ex_players.carn.player_configuration.player_id,
                                self.ex_players.carn.player_configuration)
        self.coop = SillyPlayer(self.ex_players.coop.player_configuration.player_id,
                                self.ex_players.coop.player_configuration)
        self.carn_coop = SillyPlayer(self.ex_players.carn_coop.player_configuration.player_id,
                                     self.ex_players.carn_coop.player_configuration)
        self.fat_default = SillyPlayer(self.ex_players.fat_default.player_configuration.player_id,
                                       self.ex_players.fat_default.player_configuration)
        self.fat_min = SillyPlayer(self.ex_players.fat_min.player_configuration.player_id,
                                   self.ex_players.fat_min.player_configuration)
        self.fat3 = SillyPlayer(self.ex_players.fat3.player_configuration.player_id,
                                self.ex_players.fat3.player_configuration)
        self.fat5 = SillyPlayer(self.ex_players.fat5.player_configuration.player_id,
                                self.ex_players.fat5.player_configuration)
        self.fat_max = SillyPlayer(self.ex_players.fat_max.player_configuration.player_id,
                                   self.ex_players.fat_max.player_configuration)
        self.carn_fat = SillyPlayer(self.ex_players.carn_fat.player_configuration.player_id,
                                    self.ex_players.carn_fat.player_configuration)
        self.carn_fat_coop = SillyPlayer(self.ex_players.carn_fat_coop.player_configuration.player_id,
                                         self.ex_players.carn_fat_coop.player_configuration)
        self.fora = SillyPlayer(self.ex_players.fora.player_configuration.player_id,
                                self.ex_players.fora.player_configuration)
        self.carn_fora = SillyPlayer(self.ex_players.carn_fora.player_configuration.player_id,
                                     self.ex_players.carn_fora.player_configuration)

        self.fat_and_burr_veg = SillyPlayer(self.ex_players.fat_and_burr_veg.player_configuration.player_id,
                                            self.ex_players.fat_and_burr_veg.player_configuration)
        self.fat_and_carn_coop = SillyPlayer(self.ex_players.fat_and_carn_coop.player_configuration.player_id,
                                             self.ex_players.fat_and_carn_coop.player_configuration)
        self.carn_coop_and_fat_and_fat = SillyPlayer(self.ex_players.carn_coop_and_fat_and_fat.player_configuration.player_id,
                                                     self.ex_players.carn_coop_and_fat_and_fat.player_configuration)
        self.fat_and_carn_and_shell_veg = SillyPlayer(self.ex_players.fat_and_carn_and_shell_veg.player_configuration.player_id,
                                                      self.ex_players.fat_and_carn_and_shell_veg.player_configuration)
        self.carn_and_coop_veg = SillyPlayer(self.ex_players.carn_and_coop_veg.player_configuration.player_id,
                                             self.ex_players.carn_and_coop_veg.player_configuration)

        self.carn_w_cards = SillyPlayer(self.ex_players.player_carn_w_cards.player_configuration.player_id,
                                        self.ex_players.player_carn_w_cards.player_configuration)
        self.coop_w_cards = SillyPlayer(self.ex_players.coop_w_cards.player_configuration.player_id,
                                        self.ex_players.coop_w_cards.player_configuration)