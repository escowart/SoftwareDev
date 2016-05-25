import logging

evo_print_on = False

log = logging.getLogger("Evolution Logger")


def evo_print(msg: str) -> None:
    """ Print the given string if evo print is on
    :param msg: The string message
    """
    log.info(msg)
    if evo_print_on:
        print(msg)
