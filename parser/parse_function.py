from parser.Parser import Parser
import parser.parse_expression as pe
from parser.parse_generic import parse_identifier, parse_type
from parser.parse_statement import parse_body
from util import safe_call


def parse_function(parser: Parser) -> list:
    func_name = parse_identifier(parser)
    parser.expect("(")
    params = []
    if parser.lookahead() == ")":
        parser.eat()
    else:
        while True:
            btype = pe.parse_type(parser)
            name = parse_identifier(parser)
            params.append({'type': btype, 'name': name})
            token = parser.lookahead()
            if token == ')':
                parser.eat()
                break
            parser.expect(',')
    parser.expect("=")
    parser.expect(">")
    ret_type = safe_call(parse_type, parser)
    if ret_type is None:
        parser.expect('void')
        ret_type = 'void'
    return ['FUNCTION', {'func_name': func_name, 'params': params, 'return_type': ret_type, 'body': parse_body(parser)}]
