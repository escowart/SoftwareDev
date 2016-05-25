from gui.config_gen import *

def show_configuration(configuration: Configuration) -> None:
    """ Shows the dealers GUI from a given configuration
    :param configuration that is given that shows the Dealer's state
    """
    config_igen = make_configuration_igen(configuration)

    root = tk.Tk()
    config_igen.display(root)

    root.wm_title("Evolution")
    root.mainloop()


def show_player_configuration(p_config: PlayerConfiguration) -> None:
    """ Shows the current player's gui from a given configuration
    :param p_config the given player's configuration
    """
    player = Player(p_config.player_id,
                    p_config.species_list,
                    p_config.food_bag,
                    p_config.hand)
    cur_player_igen = make_player_state_igen(player)

    root = tk.Tk()
    cur_player_igen.display(root)

    root.wm_title("Evolution")
    root.mainloop()