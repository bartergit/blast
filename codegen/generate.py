from codegen.Context import Ctx
from compiler import barter_compile


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
            return f"{generate_expression(ctx, variable)}->{field}"
        case ['CAST', [first, btype]]:
            ctype = ctx.btype_to_ctype(btype)
            return f"({ctype}){generate_expression(ctx, first)}"
        case _:
            raise Exception(expr)


def generate_variable_declaration(ctx: Ctx, dec) -> None:
    name, btype, value = dec['name'], dec['type'], generate_expression(ctx, dec['value'])
    ctype = ctx.btype_to_ctype(btype)
    ctx.add(f"{ctype} {name} = {value};")


def generate_assign(ctx: Ctx, assign_to: list, value: list) -> None:
    ctx.add(f"{generate_expression(ctx, assign_to)} = {generate_expression(ctx, value)};")


def generate_statement(ctx: Ctx, statement) -> None:
    match statement:
        case ['DECLARATION', data]:
            generate_variable_declaration(ctx, data)
        case ['ASSIGN', {'assign_to': assign_to, 'value': value}]:
            generate_assign(ctx, assign_to, value)
        case ['BREAK' | 'CONTINUE' as data]:
            ctx.add(data.lower())
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
        case other:
            generate_expression(ctx, other)


def generate_function(ctx: Ctx, function: list):
    match function:
        case ['FUNCTION', {'func_name': func_name, 'params': params, 'return_type': ret_type, 'body': body}]:
            generated_params = []
            for param in params:
                btype, name = param['type'], param['name']
                ctype = ctx.btype_to_ctype(btype)
                generated_params.append(f"{ctype} {name}")
            header = f"{ret_type} {func_name}({','.join(generated_params)})"
            ctx.header.append(header)
            ctx.add(header + "{")
            for statement in body:
                generate_statement(ctx, statement)
            ctx.add("}")


def generate(program: dict[str, list]) -> Ctx:
    ctx = Ctx()
    for include in program['includes']:
        match include:
            case ['IMPORTC', data]:
                ctx.add(f"#include <{''.join(data)}>")
            case ['IMPORT', data]:
                path = data + '.barter'
                with open(path) as f:
                    imported_ctx = barter_compile(f.read())
                    ctx.header.extend(imported_ctx.header)
                    ctx.listing.extend(imported_ctx.listing)
            case _:
                break
    for struct in program['structs']:
        match struct:
            case ['STRUCT', {'struct_name': struct_name, 'fields': fields}]:
                ctx.structs.add(struct_name)
                ctx.header.append(f"struct {struct_name}")
                ctx.add(f"struct {struct_name}{{")
                for field in fields:
                    filed_btype, field_name = field['type'], field['filed_name']
                    ctx.add(f"{ctx.btype_to_ctype(filed_btype)} {field_name};")
                ctx.add("};")
            case _:
                break
    for function in program['functions']:
        generate_function(ctx, function)
    return ctx
