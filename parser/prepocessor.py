from dataclasses import dataclass, field
from tokenize import TokenInfo

from parser.Parser import Parser
from parser.parse_generic import parse_identifier


def compile_time_body(parser: Parser, end: str = None) -> list:
    body = []
    while not parser.empty():
        token = parser.peek_token()
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
    assert condition in ['true', 'false']
    parser.expect(")")
    return ['COMPIF', {'condition': condition == 'true', 'body': compile_time_body(parser, "endif")}]


def compile_time_for(parser: Parser) -> list:
    parser.expect("(")
    parser.expect("for")
    item_name = parse_identifier(parser)
    parser.expect("in")
    parser.expect("[")
    items = parser.until_tokens("]")
    parser.expect(")")
    return ['COMPFOR', {'item_name': item_name, 'items': items, 'body': compile_time_body(parser, "endfor")}]


def unfold(tokens: list, compilation_ctx: dict) -> list[TokenInfo]:
    result = []
    for token in tokens:
        match token:
            case ['COMPIF', {'condition': condition, 'body': body}]:
                if condition:
                    result.extend(unfold(body, compilation_ctx))
            case ['COMPFOR', {'item_name': item_name, 'items': items, 'body': body}]:
                for item in items:
                    compilation_ctx[item_name] = item
                    result.extend(unfold(body, compilation_ctx))
                compilation_ctx.pop(item_name)
            case ['COMPEXPR', name]:
                result.append(compilation_ctx[name])
            case token:
                result.append(token)
    return result


def apply_preprocess(parser: Parser) -> list[TokenInfo]:
    before_i = parser.i
    body = compile_time_body(parser)
    parser.i = before_i
    return unfold(body, {})
