from typing import Callable

from parser.Parser import Parser


class AD(dict):
    def __init__(self, *args, **kwargs):
        super(AD, self).__init__(*args, **kwargs)
        self.__dict__ = self


def safe_call(function: Callable, parser: Parser):
    try:
        prev_i = parser.i
        return function(parser)
    except Exception:
        parser.i = prev_i


def safe_wrapper(functions: list[Callable], parser: Parser):
    for function in functions:
        result = safe_call(function, parser)
        if result:
            return result
    parser.err()
