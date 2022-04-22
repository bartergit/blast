from parser.Parser import Parser
from parser.parse_include import parse_include
from parser.parse_statement import parse_statement
from util import safe_call


def parse_program(parser: Parser) -> list[dict]:
    program = []
    while True:
        result = safe_call(parse_include, parser)
        if result is None:
            break
        program.append(result)
    while not parser.empty():
        program.append(parse_statement(parser))
    return program
