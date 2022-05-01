from tokenize import TokenInfo
from typing import Callable

from parser.Parser import Parser


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


def dump(tokens: list[TokenInfo]) -> list[str]:
    return [token.string for token in tokens]
