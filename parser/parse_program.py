from parser.Parser import Parser
from parser.parse_function import parse_function
from parser.parse_include import parse_include
from parser.parse_struct import parse_struct_declaration
from preprocessing.prepocessor import apply_preprocess
from util import safe_call


def get_all_includes(parser: Parser) -> list:
    includes = []
    while True:
        result = safe_call(parse_include, parser)
        if result is None:
            break
        includes.append(result)
    return includes


def get_all_structs(parser: Parser) -> list:
    structs = []
    while True:
        result = safe_call(parse_struct_declaration, parser)
        if result is None:
            break
        structs.append(result)
    return structs


def parse_program(parser: Parser) -> dict[str, list]:
    program = {'structs': [], 'includes': get_all_includes(parser), 'functions': []}
    apply_preprocess(parser)
    program['structs'] = get_all_structs(parser)
    while not parser.empty():
        program['functions'].append(parse_function(parser))
    return program
