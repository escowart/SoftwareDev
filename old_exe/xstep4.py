import json
import sys

from evo_json.all_converters import *
from evolution.dealers.dealer import Dealer


def main():
    process_json_step4(sys.stdin, sys.stdout)


def process_json_step4(file_in, file_out):
    """ Process evolution according to HW-8 Specs
    :param file_in: In file
    :param file_out: Out file
    """
    py_json_config_step4 = json.load(file_in)

    in_config = Unset   # type: Configuration
    actions = Unset     # type: List[Action]

    try:
        in_config, actions = convert_from_pj_config_and_step4(py_json_config_step4)

        dealer = Dealer(*in_config)
        dealer.step4(actions)
    except Exception as e:
        raise e


    out_config = dealer.configuration
    pj_config = convert_to_pj_config(out_config)

    json.dump(pj_config, file_out)



