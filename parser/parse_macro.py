from tokenize import TokenInfo

from parser.Parser import Parser
from parser.parse_generic import parse_identifier
from parser.tokenizer import tokenize

from jinja2.nativetypes import NativeEnvironment


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
            token = parser.peek()
            if token == ')':
                break
            parser.expect(",")
    parser.macros[macro_name] = {'args': args, 'body': parser.until("end")}


def expand_macro(parser: Parser, macro_name, args) -> list[TokenInfo]:
    macro = parser.macros[macro_name]
    body_as_str = ' '.join(macro['body']) \
        .replace("{ {", "{{") \
        .replace("} }", "}}") \
        .replace("{ %", "{%") \
        .replace("% }", "%}")
    print(body_as_str)
    result = NativeEnvironment(). \
        from_string(body_as_str) \
        .render(dict(zip(macro['args'], [' '.join(arg) for arg in args])))
    print(result)
    return tokenize(result)


def expand_macros(parser: Parser) -> bool:
    tmp = []
    i = parser.i
    while not parser.empty():
        token = parser.peek_token()
        if token.string == "mcall":
            macro_name = parser.peek()
            parser.expect("(")
            args = []
            arg = []
            while True:
                token = parser.peek()
                if token == ",":
                    args.append(arg)
                    continue
                if token == ')':
                    args.append(arg)
                    tmp.extend(expand_macro(parser, macro_name, args))
                    break
                arg.append(token)
        else:
            tmp.append(token)
    parser.tokens[i + 1:] = tmp
    parser.i = i
    return True
