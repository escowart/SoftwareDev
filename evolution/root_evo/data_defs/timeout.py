import threading
from functools import wraps
from evolution.root_evo.data_defs.type_value import *
from evolution.root_evo.data_defs.natural import *

class TimeoutDecoratorError(Exception):
    """ A Timeout Error """


R = TypeVar('R')   # The return type of a Decorator
Decorator = Any    # The Decorator type


class NoResult(NoValue):
    """ A No Result from a Timeout Thread """


class TimeoutThread(threading.Thread):
    """ A Thread which can be used to timeout """
    def __init__(self, func, *args, **kwargs) -> None:
        """ Construct a Timeout Thread
        :param func: The function being called
        :param args: The arguments
        :param kwargs: The key word arguments
        """
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = NoResult

    def run(self) -> None:
        """ Call the function with the arguments to get the result
        Effect: Modifies the result of the function call
        """
        try:
            self.result = self.func(*self.args, **self.kwargs)
        except Exception as e:
            self.result = NoResult


def timeout(seconds: Natural) -> Decorator:
    """ The timeout decorator definition
    :param seconds: The number of seconds the timeout will wait
    :return: The resulting timeout decorator
    """
    def decorator(func) -> R:
        """ Decorator returns the func's result or raises a TimeoutError
        :param func: The function that is being wrapped
        :return: The result of the TimeoutThread
        :raises: TimeoutError if the TimeoutThread returns NoResult
        """
        def wrapper(*args, **kwargs) -> R:
            """ The timeout wrapper """
            timeout_thread = TimeoutThread(func, *args, **kwargs)
            timeout_thread.start()
            timeout_thread.join(seconds)

            if timeout_thread.is_alive():
                raise TimeoutDecoratorError("Thread Still Running")

            result = timeout_thread.result
            if result == NoResult:
                raise TimeoutDecoratorError("No Result from Thread")

            return result

        return wraps(func)(wrapper)

    return decorator
