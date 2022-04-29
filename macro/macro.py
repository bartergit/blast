from parser.Parser import Parser
from parser.parse_generic import parse_identifier


def loop(parser: Parser):
    parser.expect("#")
    parser.expect("for")
    item = parse_identifier(parser)
    parser.expect("in")
    collection = parse_identifier(parser)
    parser.until("#endfor")


if __name__ == '__main__':
    f("hello")
