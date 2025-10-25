import ply.yacc as yacc
from lexer_rules import tokens

# Regras da gramática
def p_program(p):
    'program : stmt_list'
    p[0] = ('program', p[1])

def p_stmt_list(p):
    '''stmt_list : stmt
                 | stmt_list SEMI stmt'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_stmt(p):
    '''stmt : os_cmd
            | ia_cmd
            | meta_cmd'''
    p[0] = p[1]

def p_os_cmd(p):
    '''os_cmd : IDENT args_opt'''
    p[0] = ('os_cmd', p[1], p[2])

def p_args_opt(p):
    '''args_opt : args
                | empty'''
    p[0] = p[1]

def p_args(p):
    '''args : arg
            | args arg'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_arg(p):
    '''arg : IDENT
           | STRING
           | PATH'''
    p[0] = ('arg', p[1])

def p_ia_cmd(p):
    '''ia_cmd : IA ASK STRING
              | IA SUMMARIZE STRING
              | IA CODEEXPLAIN FILENAME'''
    p[0] = ('ia_cmd', p[1], p[2], p[3])

def p_meta_cmd(p):
    '''meta_cmd : CD PATH
                | PWD
                | HISTORY'''
    p[0] = ('meta_cmd', p[1:] if len(p) > 2 else (p[1],))

def p_empty(p):
    'empty :'
    p[0] = []

def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}'")
    else:
        print("Erro de sintaxe no final da entrada")

parser = yacc.yacc()
