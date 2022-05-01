from parser.Parser import Parser
from parser.parse_include import parse_include
from parser.parse_macro import parse_macro_declaration, expand_macros
from parser.parse_statement import parse_statement
from parser.parse_struct import parse_struct_declaration
from util import safe_call


def parse_program(parser: Parser) -> list[dict]:
    program = []
    while True:
        result = safe_call(parse_include, parser)
        if result is None:
            break
        program.append(result)
    while True:
        result = safe_call(parse_macro_declaration, parser)
        if not result:
            break
    expand_macros(parser)
    while True:
        result = safe_call(parse_struct_declaration, parser)
        if result is None:
            break
        program.append(result)
    while not parser.empty():
        statement = parse_statement(parser)
        if statement != ['EMPTY']:
            program.append(statement)
    return program
