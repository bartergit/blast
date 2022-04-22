from parser.Parser import Parser
from parser.builtin import binary_operators
from parser.parse_func_call import parse_func_call
from parser.parse_generic import parse_identifier
from util import safe_wrapper


def parse_variable_use(parser: Parser) -> list:
    return ['VARIABLE', parse_identifier(parser)]


def parse_binary_operator(parser: Parser) -> str:
    operator = parser.peek()
    assert operator in binary_operators
    return operator


def parse_number(parser: Parser) -> list:
    number = parser.peek()
    assert number.isdigit()
    return ['NUMBER', number]


def parse_atom(parser: Parser) -> str:
    return safe_wrapper([parse_func_call, parse_number, parse_variable_use], parser)


def parse_binary_expression(parser: Parser) -> list:
    first = parse_atom(parser)
    operator = parse_binary_operator(parser)
    second = parse_atom(parser)
    return ['BINARY', [operator, first, second]]


def parse_expression(parser: Parser) -> dict:
    return safe_wrapper([parse_binary_expression, parse_atom], parser)
