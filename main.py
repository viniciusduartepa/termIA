import os

from lexer_rules import lexer
from parser_rules import parser
from meta_cmd_handler import MetaCmdHandler
from ia_cmd_handler import IACmdHandler

from completion import setup_readline, build_default_commands 



custom_commands = build_default_commands()
setup_readline(custom_commands)


meta_handler = MetaCmdHandler()
ia_handler = IACmdHandler()


while True:
    try:
        prompt = f'{os.getcwd()} > '
        data = input(prompt)
    except EOFError:
        break

    if not data:
        continue

    meta_handler.add_to_history(data)

    result = parser.parse(data, lexer=lexer)

    if not result:
        continue

    if result[0] == 'program':
        stmts = result[1]
    else:
        stmts = [result]

    for stmt in stmts:
        if isinstance(stmt, tuple) and stmt:
            tag = stmt[0]

            if tag == 'meta_cmd':
                out = meta_handler.handle(stmt)
                if out is not None:
                    print(out)
                continue

            if tag == 'ia_cmd':
                out = ia_handler.handle(stmt)
                if out is not None:
                    print(out)
                continue

        print("Comando nao reconhecido")
