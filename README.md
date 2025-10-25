# TermIA - Shell Inteligente com Técnicas de Compiladores

## Introdução

O **TermIA** é um terminal inteligente desenvolvido como projeto da disciplina ECOI26 – Compiladores. Ele combina conceitos de compiladores com integração de Inteligência Artificial, permitindo que o usuário execute comandos tradicionais de terminal, além de comandos especiais que utilizam IA para fornecer respostas dinâmicas, resumos de textos ou explicações de códigos.

### Ferramentas Utilizadas

- **Python**: Linguagem principal do projeto.
- **PLY (Python Lex-Yacc)**: Para a implementação do lexer e parser.

## Gramática do TermIA

A gramática define a estrutura dos comandos que o terminal reconhece:

```text
program    := stmt_list EOF
stmt_list  := stmt (';' stmt)*
stmt       := os_cmd | ia_cmd | meta_cmd
os_cmd     := IDENT arg*
arg        := IDENT | STRING | PATH
ia_cmd     := 'ia' ( 'ask' STRING
                   | 'summarize' STRING
                   | 'codeexplain' FILENAME )
meta_cmd   := 'cd' PATH | 'pwd' | 'history'
```

### Programa
**program**: Programa completo, composto por uma lista de comandos seguida do fim da entrada (EOF).

### Lista de Comandos
**stmt_list**: Lista de comandos, separados opcionalmente por `;`.

### Comando
**stmt**: Um comando individual, que pode ser:

- **os_cmd**: Comando do sistema com argumentos opcionais.
- **ia_cmd**: Comando que interage com a IA (`ask`, `summarize`, `codeexplain`).
- **meta_cmd**: Comando interno do terminal (`cd`, `pwd`, `history`).

### Argumentos
**arg**: Argumentos de um comando (`IDENT`, `STRING` ou `PATH`).

## Como Executar

### Clonar o repositório

```bash
git clone https://github.com/seu-usuario/TermIA.git
cd TermIA
```

### Criar e ativar ambiente virtual (opcional, mas recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
### Instalar dependências

```bash
pip install -r requirements.txt
```
### Executar o terminal interativo
```bash
python main.py
```

### Exemplo de comandos

```text
>> ls
>> ia ask "Qual é a capital da França?"
>> cd /home/usuario
>> pwd
>> history
```
