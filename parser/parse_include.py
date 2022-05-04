from parser.Parser import Parser
from util import safe_wrapper


def parse_importc(parser: Parser):
    parser.expect("importc")
    parser.expect("<")
    return ['IMPORTC', parser.until(">")]


def parse_native_import(parser: Parser):
    parser.expect("import")
    token = parser.peek()
    assert token.startswith('"') and token.endswith('"'), token
    return ['IMPORT', token[1:-1]]


def parse_include(parser: Parser):
    return safe_wrapper([parse_importc, parse_native_import], parser)
