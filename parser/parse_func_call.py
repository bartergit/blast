from parser.Parser import Parser
import parser.parse_expression as pe
from parser.parse_generic import parse_identifier


def parse_func_call(parser: Parser) -> list:
    parser.expect("call")
    func_name = parse_identifier(parser)
    parser.expect("(")
    exprs = []
    if parser.lookahead() == ")":
        parser.eat()
        return ['CALL', {'func_name': func_name, 'args': exprs}]
    while True:
        expr = pe.parse_expression(parser)
        exprs.append(expr)
        token = parser.lookahead()
        if token == ')':
            parser.eat()
            return ['CALL', {'func_name': func_name, 'args': exprs}]
        parser.expect(',')
