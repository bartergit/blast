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
    assign_to = parse_expression(parser)
    parser.expect("=")
    value = parse_expression(parser)
    parser.expect(";")
    return ['ASSIGN', {'assign_to': assign_to, 'value': value}]


def parse_inline_c(parser: Parser) -> list:
    parser.expect("`")
    return ['INLINE', parser.until("`")]


def parse_body(parser: Parser) -> list:
    parser.expect("{")
    body = []
    while True:
        result = safe_call(parse_statement, parser)
        if result is None:
            parser.expect("}")
            return body
        body.append(result)


def parse_if(parser: Parser) -> list:
    parser.expect("if")
    condition = parse_expression(parser)
    return ['IF', {'condition': condition, 'body': parse_body(parser)}]


def parse_loop(parser: Parser) -> list:
    parser.expect("while")
    condition = parse_expression(parser)
    return ['WHILE', {'condition': condition, 'body': parse_body(parser)}]


def parse_empy_statement(parser: Parser):
    parser.expect(";")
    return ['EMPTY']


def parse_return(parser: Parser):
    parser.expect("ret")
    expr = parse_expression(parser)
    return ['RETURN', expr]


def parse_loop_statements(parser: Parser):
    token = parser.peek()
    if token in ('break', 'continue'):
        return [token.upper()]
    assert 0, token


def parse_statement(parser: Parser) -> list:
    return safe_wrapper(
        [parse_return,
         parse_loop_statements,
         parse_assign,
         parse_declaration,
         parse_inline_c,
         parse_loop,
         parse_if,
         parse_expression,
         parse_empy_statement],
        parser)
