import ply.yacc as yacc
from lexer_rules import tokens

# -----------------------------
# Regras da gramática
# -----------------------------

def p_program(p):
    """program : stmt_list"""
    p[0] = ('program', p[1])


def p_stmt_list(p):
    """
    stmt_list : stmt
              | stmt_list SEMI stmt
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_stmt(p):
    """
    stmt : os_cmd
         | ia_cmd
         | meta_cmd
    """
    p[0] = p[1]


# -----------------------------
# OS CMD (comandos normais)
# -----------------------------

def p_os_cmd(p):
    """os_cmd : IDENT args_opt"""
    p[0] = ('os_cmd', p[1], p[2])


def p_args_opt(p):
    """
    args_opt : args
             | empty
    """
    p[0] = p[1]


def p_args(p):
    """
    args : arg
         | args arg
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_arg(p):
    """
    arg : IDENT
        | STRING
        | PATH
    """
    p[0] = ('arg', p[1])


# -----------------------------
# IA CMD
# -----------------------------

def p_ia_cmd(p):
    """
    ia_cmd : IA ASK STRING
           | IA SUMMARIZE STRING
           | IA CODEEXPLAIN FILENAME
           | IA TRANSLATE STRING
           | IA DOC FILENAME
    """
    p[0] = ('ia_cmd', p[1], p[2], p[3])



# -----------------------------
# META CMD
# -----------------------------

def p_meta_cmd(p):
    '''meta_cmd : CD PATH
                | PWD
                | HISTORY
                | LS
                | LS PATH
                | TOUCH PATH
                | TOUCH FILENAME
                | RM PATH
                | RM FILENAME
                | CAT PATH
                | CAT FILENAME
                | ECHO STRING GT PATH
                | ECHO STRING GT FILENAME
                | ECHO STRING GTGT PATH
                | ECHO STRING GTGT FILENAME
                | MKDIR PATH
                | MKDIR IDENT
                | RMDIR PATH
                | RMDIR IDENT
                | CP PATH PATH
                | CP FILENAME FILENAME
                | CP FILENAME PATH
                | CP PATH FILENAME
                | MV PATH PATH
                | MV FILENAME FILENAME
                | MV FILENAME PATH
                | MV PATH FILENAME
                | WHOAMI
                | DATE
                | CLEAR
                | EXIT
    '''


    # p[1] é o lexema: 'cd', 'pwd', 'history', 'ls', 'touch', 'rm', 'cat', 'echo', 'mkdir', 'rmdir'
    cmd = p[1]

    if cmd == 'cd':
        p[0] = ('meta_cmd', 'cd', p[2])

    elif cmd == 'pwd':
        p[0] = ('meta_cmd', 'pwd')

    elif cmd == 'history':
        p[0] = ('meta_cmd', 'history')

    elif cmd == 'ls':
        if len(p) == 2:
            p[0] = ('meta_cmd', 'ls')
        else:
            p[0] = ('meta_cmd', 'ls', p[2])

    elif cmd == 'touch':
        p[0] = ('meta_cmd', 'touch', p[2])

    elif cmd == 'rm':
        p[0] = ('meta_cmd', 'rm', p[2])

    elif cmd == 'cat':
        p[0] = ('meta_cmd', 'cat', p[2])

    elif cmd == 'echo':
        text = p[2]
        op = p[3]      # '>' ou '>>'
        target = p[4]  # PATH ou FILENAME
        mode = 'write' if op == '>' else 'append'
        p[0] = ('meta_cmd', 'echo', text, mode, target)

    elif cmd == 'mkdir':
        p[0] = ('meta_cmd', 'mkdir', p[2])

    elif cmd == 'rmdir':
        p[0] = ('meta_cmd', 'rmdir', p[2])
    
    elif cmd == 'cp':
        p[0] = ('meta_cmd', 'cp', p[2], p[3])

    elif cmd == 'mv':
        p[0] = ('meta_cmd', 'mv', p[2], p[3])
    
    elif cmd == 'whoami':
        p[0] = ('meta_cmd', 'whoami')

    elif cmd == 'date':
        p[0] = ('meta_cmd', 'date')



    """
    meta_cmd : CD PATH
             | PWD
             | HISTORY
             | LS
             | LS PATH
             | TOUCH PATH
             | TOUCH FILENAME
             | RM PATH
             | RM FILENAME
             | CAT PATH
             | CAT FILENAME
             | ECHO STRING GT PATH
             | ECHO STRING GT FILENAME
             | ECHO STRING GTGT PATH
             | ECHO STRING GTGT FILENAME
    """
    cmd = p[1]

    if cmd == 'cd':
        p[0] = ('meta_cmd', 'cd', p[2])

    elif cmd == 'pwd':
        p[0] = ('meta_cmd', 'pwd')

    elif cmd == 'history':
        p[0] = ('meta_cmd', 'history')

    elif cmd == 'ls':
        if len(p) == 2:
            p[0] = ('meta_cmd', 'ls')
        else:
            p[0] = ('meta_cmd', 'ls', p[2])

    elif cmd == 'touch':
        p[0] = ('meta_cmd', 'touch', p[2])

    elif cmd == 'rm':
        p[0] = ('meta_cmd', 'rm', p[2])

    elif cmd == 'cat':
        p[0] = ('meta_cmd', 'cat', p[2])

    elif cmd == 'echo':
        text = p[2]
        op = p[3]      # > ou >>
        target = p[4]  # PATH ou FILENAME
        mode = 'write' if op == '>' else 'append'
        p[0] = ('meta_cmd', 'echo', text, mode, target)
    
    elif cmd == 'clear':
        p[0] = ('meta_cmd', 'clear')

    elif cmd == 'exit':
        p[0] = ('meta_cmd', 'exit')


# -----------------------------
# EMPTY
# -----------------------------

def p_empty(p):
    """empty :"""
    p[0] = []


# -----------------------------
# ERRO
# -----------------------------

def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}'")
    else:
        print("Erro de sintaxe no final da entrada")


# -----------------------------
# BUILD DO PARSER
# -----------------------------
parser = yacc.yacc()
