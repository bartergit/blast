from parser.Parser import Parser
from parser.parse_expression import parse_expression
from parser.parse_generic import parse_type, parse_identifier
from util import safe_wrapper, safe_call


def parse_declaration(parser: Parser) -> list:
    btype = parse_type(parser)
    var_name = parse_identifier(parser)
    parser.expect("=")
    value = parse_expression(parser)
    parser.expect(";")
    return ['DECLARATION', {'type': btype, 'name': var_name, 'value': value}]


def parse_assign(parser: Parser) -> list:
    var_name = parse_identifier(parser)
    parser.expect("=")
    value = parse_expression(parser)
    parser.expect(";")
    return ['ASSIGN', {'name': var_name, 'value': value}]


def parse_inline_c(parser: Parser) -> list:
    parser.expect("`")
    return ['INLINE', parser.until("`")]


def parse_loop(parser: Parser) -> list:
    parser.expect("while")
    condition = parse_expression(parser)
    parser.expect("{")
    body = []
    while True:
        result = safe_call(parse_statement, parser)
        if result is None:
            parser.expect("}")
            return ['WHILE', {'condition': condition, 'body': body}]
        body.append(result)


def parse_if(parser: Parser) -> list:
    parser.expect("if")
    condition = parse_expression(parser)
    parser.expect("{")
    body = []
    while True:
        result = safe_call(parse_statement, parser)
        if result is None:
            parser.expect("}")
            return ['IF', {'condition': condition, 'body': body}]
        body.append(result)


def parse_empy_statement(parser: Parser):
    parser.expect(";")
    return ['EMPTY']


def parse_statement(parser: Parser) -> list:
    return safe_wrapper(
        [parse_assign, parse_declaration, parse_inline_c, parse_loop, parse_if, parse_empy_statement],
        parser)
