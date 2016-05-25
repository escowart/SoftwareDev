import json
import sys
from evo_json.convert_py_json.convert_config import *
from gui.config_gen import *


def main():
    run_gui(sys.stdin, sys.stdout)


def run_gui(file_in, file_out):
    """ Process evolution according to HW-9 Specs and Run the GUI
    :param file_in: In file
    :param file_out: Out file
    """
    py_json_config = json.load(file_in)

    try:
        # Convert PyJSON Configuration -> Configuration
        in_config = convert_from_pj_config(py_json_config)
    except ValueError as e:
        # Error forming the Configuration => Invalid input Configuration
        return

    config_igen = make_configuration_igen(in_config)
    cur_player_igen = make_player_state_igen(in_config.player_sequence[0])

    root = tk.Tk()
    cur_player_igen.display(root)
    root = tk.Tk()
    config_igen.display(root)

    root.wm_title("Evolution")
    root.mainloop()