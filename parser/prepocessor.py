from tokenize import TokenInfo

import parser.parse_macro as macro
from parser.Parser import Parser
from parser.parse_generic import parse_identifier
from util import safe_call, dump


def compile_time_body(parser: Parser, end: str = None) -> list:
    body = []
    while not parser.empty():
        token = parser.peek_token()
        if token.string == "end" and end == "end":
            return body
        if token.string != "$":
            body.append(token)
            continue
        token = parser.lookahead()
        if token != "(":
            body.append(['COMPEXPR', token])
            parser.eat()
            continue
        if parser.lookahead(1) == end:
            parser.eat(2)
            parser.expect(")")
            return body
        match parser.lookahead(1):
            case "if":
                body.append(compile_time_if(parser))
            case "for":
                body.append(compile_time_for(parser))
            case item:
                body.append(['COMPEXPR', item])
                parser.eat(2)
                parser.expect(")")
                # compile_time_expr(parser)
    if end is None:
        return body
    assert 0


def compile_time_if(parser: Parser) -> list:
    parser.expect("(")
    parser.expect("if")
    condition = parser.peek()
    parser.expect(")")
    body = compile_time_body(parser, "endif")
    return ['COMPIF', {'condition': condition, 'body': body}]


def compile_time_for(parser: Parser) -> list:
    parser.expect("(")
    parser.expect("for")
    item_name = parse_identifier(parser)
    parser.expect("in")
    items = parse_identifier(parser)
    parser.expect(")")
    body = compile_time_body(parser, "endfor")
    return ['COMPFOR', {'item_name': item_name, 'items': items, 'body': body}]


def unfold(tokens: list, compilation_ctx: dict) -> list[TokenInfo]:
    result = []
    for token in tokens:
        match token:
            case ['COMPIF', {'condition': condition, 'body': body}]:
                if compilation_ctx[condition]:
                    result.extend(unfold(body, compilation_ctx))
            case ['COMPFOR', {'item_name': item_name, 'items': items, 'body': body}]:
                for item in compilation_ctx[items]:
                    compilation_ctx[item_name] = [item]
                    result.extend(unfold(body, compilation_ctx))
                compilation_ctx.pop(item_name)
            case ['COMPEXPR', name]:
                result.extend(compilation_ctx[name])
            case token:
                result.append(token)
    return result


def parse_all_macro_declarations(parser: Parser) -> None:
    while True:
        result = safe_call(macro.parse_macro_declaration, parser)
        if not result:
            break


def apply_preprocess(parser: Parser):
    parse_all_macro_declarations(parser)
    macro.expand_macros(parser)
