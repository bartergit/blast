from codegen.Context import Ctx


def generate_expression(ctx: Ctx, expr) -> str:
    match expr:
        case ['NUMBER', number]:
            return number
        case ['VARIABLE', variable]:
            return variable
        case ['BINARY', [operator, first, second]]:
            return f"{generate_expression(ctx, first)} {operator} {generate_expression(ctx, second)}"
        case ['CALL', {'func_name': func_name, 'args': args}]:
            return f"{func_name}({','.join([generate_expression(ctx, arg) for arg in args])})"
        case _:
            raise Exception(expr)


def generate_declaration(ctx: Ctx, dec) -> None:
    name, btype, value = dec['name'], dec['type'], generate_expression(ctx, dec['value'])
    ctx.add(f"{btype} {name} = {value};")


def generate_statement(ctx: Ctx, statement) -> None:
    match statement:
        case ['DECLARATION', data]:
            generate_declaration(ctx, data)
        case ['INLINE', data]:
            ctx.add(' '.join(data))
        case _:
            raise Exception(statement)


def generate(program: list[dict]) -> str:
    ctx = Ctx()
    for i, statement in enumerate(program):
        match statement:
            case['IMPORTC', data]:
                ctx.add(f"#include <{''.join(data)}>")
            case _:
                break
    ctx.add("int main(){")
    for statement in program[i:]:
        generate_statement(ctx, statement)
    ctx.add("}")
    return 'using std::make_unique;' + '\n'.join(ctx.listing)
