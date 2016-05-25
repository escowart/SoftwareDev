from abc import ABCMeta, abstractmethod
from typing import TypeVar, Any, Tuple, Union, Generic, Callable, cast
from collections import namedtuple
from copy import deepcopy, copy

Item = TypeVar('Item')

StrJSON = str
