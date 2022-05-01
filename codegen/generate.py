from codegen.Context import Ctx
from parser.builtin import btype_to_ctype


def generate_expression(ctx: Ctx, expr) -> str:
    match expr:
        case ['NUMBER', number]:
            return number
        case ['BOOL', boolean]:
            return boolean
        case ['VARIABLE', variable]:
            return variable
        case ['BINARY', [operator, first, second]]:
            return f"{generate_expression(ctx, first)} {operator} {generate_expression(ctx, second)}"
        case ['CALL', {'func_name': func_name, 'args': args}]:
            return f"{func_name}({','.join([generate_expression(ctx, arg) for arg in args])})"
        case ['FIELD', {'variable': variable, 'field_name': field}]:
            return f"{generate_expression(ctx, variable)}.{field}"
        case ['CAST', [first, btype]]:
            ctype = btype_to_ctype.get(btype, btype)
            return f"({ctype}){generate_expression(ctx, first)}"
        case _:
            raise Exception(expr)


def generate_variable_declaration(ctx: Ctx, dec) -> None:
    name, btype, value = dec['name'], dec['type'], generate_expression(ctx, dec['value'])
    ctype = btype_to_ctype.get(btype, btype)
    ctx.add(f"{ctype} {name} = {value};")


def generate_assign(ctx: Ctx, dec) -> None:
    name, value = dec['name'], generate_expression(ctx, dec['value'])
    ctx.add(f"{name} = {value};")


def generate_statement(ctx: Ctx, statement) -> None:
    match statement:
        case ['DECLARATION', data]:
            generate_variable_declaration(ctx, data)
        case ['ASSIGN', data]:
            generate_assign(ctx, data)
        case ['INLINE', data]:
            ctx.add(' '.join(data))
        case ['WHILE' | 'IF' as tag, {'condition': expr, 'body': body}]:  # if, while
            ctx.add(f"{tag.lower()} ({generate_expression(ctx, expr)}) {{")
            for statement in body:
                generate_statement(ctx, statement)
            ctx.add("}")
        case ['RETURN', expr]:
            ctx.add(f"return {generate_expression(ctx, expr)};")
        case ['EMPTY']:
            pass
        case _:
            raise Exception(statement)


def generate_function(ctx: Ctx, function: list):
    match function:
        case ['FUNCTION', {'func_name': func_name, 'params': params, 'return_type': ret_type, 'body': body}]:
            generated_params = []
            for param in params:
                btype, name = param['type'], param['name']
                ctype = btype_to_ctype.get(btype, btype)
                generated_params.append(f"{ctype} {name}")
            ctx.add(f"{ret_type} {func_name}({','.join(generated_params)}){{")
            for statement in body:
                generate_statement(ctx, statement)
            ctx.add("}")


def generate(program: dict[str, list]) -> str:
    ctx = Ctx()
    for include in program['includes']:
        match include:
            case ['IMPORTC', data]:
                ctx.add(f"#include <{''.join(data)}>")
            case _:
                break
    for struct in program['structs']:
        match struct:
            case ['STRUCT', {'struct_name': struct_name, 'fields': fields}]:
                ctx.add(f"struct {struct_name}{{")
                for field in fields:
                    filed_btype, field_name = field['type'], field['filed_name']
                    ctx.add(f"{filed_btype} {field_name};")
                ctx.add("};")
            case _:
                break
    for function in program['functions']:
        generate_function(ctx, function)
    return '\n'.join(ctx.listing)
