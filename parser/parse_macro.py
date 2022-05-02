from tokenize import TokenInfo

from parser.Parser import Parser
from parser.parse_generic import parse_identifier
from parser.prepocessor import compile_time_body, unfold
from parser.tokenizer import tokenize
from util import foreach


def parse_macro_declaration(parser: Parser):
    parser.expect("macro")
    macro_name = parse_identifier(parser)

    parser.expect("(")
    args = []
    if parser.lookahead() == ")":
        parser.eat()
    else:
        while True:
            args.append(parse_identifier(parser))
            token = parser.lookahead()
            if token == ')':
                parser.eat()
                break
            parser.expect(",")
    macro_parser = Parser(parser.until_tokens("end"))
    parser.macros[macro_name] = {'args': args, 'body': compile_time_body(macro_parser)}
    print('here')
    return True


def expand_macro(macro, callee_args):
    compilation_ctx = dict(zip(macro['args'], callee_args))
    return unfold(macro['body'], compilation_ctx)


def parse_arguments(parser: Parser) -> list:
    args = []
    arg = []
    while True:
        token = parser.peek_token()
        if token.string == "[":
            arg.extend(parser.until_tokens("]"))
            continue
        if token.string == ",":
            args.append(arg.copy())
            arg.clear()
            continue
        if token.string == ')':
            args.append(arg)
            return args
        arg.append(token)


def expand_macros(parser: Parser) -> None:  # TODO: change this code
    tmp = []
    before_i = parser.i
    while not parser.empty():
        token = parser.peek_token()
        if token.string == "mcall":
            macro_name = parser.peek()
            parser.expect("(")
            args = parse_arguments(parser)
            tmp.extend(expand_macro(parser.macros[macro_name], args))
        else:
            tmp.append(token)
    parser.tokens[before_i + 1:] = tmp
    parser.i = before_i
