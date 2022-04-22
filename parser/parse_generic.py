from parser.Parser import Parser
from parser.builtin import btypes


def parse_identifier(parser: Parser) -> str:
    ident = parser.peek()
    assert ident.isidentifier()
    return ident


def parse_type(parser: Parser) -> str:
    btype = parser.peek()
    assert btype in btypes, btype
    return btype

