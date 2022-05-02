from parser.Parser import Parser
from parser.parse_generic import parse_type, parse_identifier


def parse_struct_declaration(parser: Parser) -> list:
    parser.expect("struct")
    struct_name = parse_identifier(parser)
    parser.structs.add(struct_name)
    parser.expect("{")
    fields = []
    while True:
        filed_btype = parse_type(parser)
        filed_name = parse_identifier(parser)
        fields.append({'type': filed_btype, 'filed_name': filed_name})
        parser.expect(';')
        if parser.lookahead() == '}':
            parser.eat()
            return ['STRUCT', {'struct_name': struct_name, 'fields': fields}]
