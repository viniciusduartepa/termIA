from lexer_rules import lexer
from parser_rules import parser

while True:
    try:
        data = input('>> ')
    except EOFError:
        break
    if not data:
        continue

    result = parser.parse(data, lexer=lexer)
    print(result)
