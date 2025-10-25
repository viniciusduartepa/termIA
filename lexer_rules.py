import ply.lex as lex

# Lista de tokens
tokens = (
    'IDENT',
    'STRING',
    'PATH',
    'FILENAME',
    'IA',
    'ASK',
    'SUMMARIZE',
    'CODEEXPLAIN',
    'CD',
    'PWD',
    'HISTORY',
    'SEMI',
)

# Palavras reservadas (para IA e meta comandos)
reserved = {
    'ia': 'IA',
    'ask': 'ASK',
    'summarize': 'SUMMARIZE',
    'codeexplain': 'CODEEXPLAIN',
    'cd': 'CD',
    'pwd': 'PWD',
    'history': 'HISTORY',
}

# Expressões regulares simples
t_SEMI = r';'

# Expressão para STRING (ex: "texto aqui")
t_STRING = r'\"([^\\\"]|\\.)*\"'

# PATH (ex: /home/user ou C:\Users\)
t_PATH = r'(/[a-zA-Z0-9_\-\.]+)+|([A-Za-z]:\\[A-Za-z0-9_\\\-\.]+)'

# IDENT (usado para nomes de comandos ou args)
def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENT')  # Checa se é palavra reservada
    return t

# FILENAME (qualquer coisa com extensão)
def t_FILENAME(t):
    r'[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9]+'
    return t

# Ignorar espaços e tabs
t_ignore = ' \t'

# Contar linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Erros léxicos
def t_error(t):
    print(f"Caractere inválido: '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
