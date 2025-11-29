import ply.lex as lex

tokens = (
    'PATH',
    'IDENT',
    'STRING',
    'FILENAME',
    'IA',
    'ASK',
    'SUMMARIZE',
    'CODEEXPLAIN',
    'TRANSLATE', 
    'DOC',   
    'CD',
    'PWD',
    'HISTORY',
    'LS',
    'TOUCH',
    'RM',
    'CAT',
    'ECHO',
    'MKDIR',
    'RMDIR',
    'CP',
    'MV',
    'WHOAMI',
    'DATE',
    'CLEAR',
    'EXIT',
    'GT',
    'GTGT',
    'SEMI',
)




reserved = {
    'ia': 'IA',
    'ask': 'ASK',
    'summarize': 'SUMMARIZE',
    'codeexplain': 'CODEEXPLAIN',
    'translate': 'TRANSLATE',   
    'doc': 'DOC',               
    'cd': 'CD',
    'pwd': 'PWD',
    'history': 'HISTORY',
    'ls': 'LS',
    'touch': 'TOUCH',
    'rm': 'RM',
    'cat': 'CAT',
    'echo': 'ECHO',
    'mkdir': 'MKDIR',
    'rmdir': 'RMDIR',
    'cp': 'CP',
    'mv': 'MV',
    'whoami': 'WHOAMI',
    'date': 'DATE',
    'clear': 'CLEAR',  
    'exit': 'EXIT',    
}



# ordem importa: primeiro >> depois >
t_GTGT = r'>>'
t_GT = r'>'
t_SEMI = r';'

t_STRING = r'\"([^\\\"]|\\.)*\"'

# 1) FILENAME – tem extensão obrigatória, opcionalmente com caminho na frente
def t_FILENAME(t):
    r'(\.{1,2}/)?[a-zA-Z0-9_\-\.]+(/[a-zA-Z0-9_\-\.]+)*\.[a-zA-Z0-9]+'
    return t

# 2) PATH – tem que ter pelo menos uma barra
def t_PATH(t):
    r'(\.{1,2}/[a-zA-Z0-9_\-\.]+(/[a-zA-Z0-9_\-\.]+)*/?)|(/[a-zA-Z0-9_\-\.]+(/[a-zA-Z0-9_\-\.]+)*/?)'
    return t

# 3) IDENT – comandos e palavras "simples"
def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENT')
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere inválido: '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
