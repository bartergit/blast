from parser.Parser import Parser
from parser.builtin import btypes
from util import dump


def parse_identifier(parser: Parser) -> str:
    temp = [parser.peek()]
    while parser.lookahead() == "_":
        parser.eat()
        temp.append(parser.peek())
    ident = '_'.join(temp)
    assert ident.isidentifier(), (dump(parser.tokens[parser.i:parser.i + 10]))
    return ident


def parse_type(parser: Parser) -> str:
    btype = parser.peek()
    assert btype in btypes or btype in parser.structs, btype
    return btype
