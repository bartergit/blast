from parser.Parser import Parser
from parser.builtin import btypes


def parse_identifier(parser: Parser) -> str:
    temp = [parser.peek()]
    while parser.lookahead() == "_":
        parser.eat()
        temp.append(parser.peek())
    ident = '_'.join(temp)
    assert ident.isidentifier()
    return ident


def parse_type(parser: Parser) -> str:
    btype = parser.peek()
    assert btype in btypes, btype
    return btype
