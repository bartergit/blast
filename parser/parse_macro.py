from tokenize import TokenInfo

from parser.Parser import Parser
from parser.parse_generic import parse_identifier
from parser.tokenizer import tokenize


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
    parser.macros[macro_name] = {'args': args, 'body': parser.until_tokens("end")}
    return True


def unsafe_interpolate_string(s: str, args: dict) -> str:
    vars().update(args)
    return eval(f'f"{s}"')


def foreach(s, iterable):
    return ''.join([eval(f'f"{s}"') for it in iterable])


def expand_macro(parser: Parser, macro_name, args) -> list[TokenInfo]:
    macro = parser.macros[macro_name]
    args_as_dict = dict(zip(macro['args'], [' '.join(arg) for arg in args]))
    vars().update(args_as_dict)
    temp = []
    for token in macro['body']:
        if token.string.startswith('f"'):
            tokens = tokenize(eval(token.string))
            temp.extend(tokens)
        else:
            temp.append(token)
    result = temp.copy()
    temp.clear()
    for token in result:
        if token.string.startswith('"'):
            temp.extend(tokenize(token.string[1:-1]))
        else:
            temp.append(token)
    return temp


def expand_macros(parser: Parser) -> bool:  # Буквально худший код на свете
    flag = True
    while flag:
        flag = False
        tmp = []
        i = parser.i
        while not parser.empty():
            token = parser.peek_token()
            if token.string == "mcall":
                flag = True
                macro_name = parser.peek()
                parser.expect("(")
                args = []
                arg = []
                while True:
                    token = parser.peek()
                    if token == ",":
                        args.append(arg.copy())
                        arg.clear()
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
