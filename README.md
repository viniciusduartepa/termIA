# TermIA - Shell Inteligente com Técnicas de Compiladores

## Introdução

O **TermIA** é um terminal inteligente desenvolvido como projeto da disciplina ECOI26 – Compiladores. Ele combina conceitos de compiladores com integração de Inteligência Artificial, permitindo que o usuário execute comandos tradicionais de terminal, além de comandos especiais que utilizam IA para fornecer respostas dinâmicas, resumos de textos ou explicações de códigos.

### Ferramentas Utilizadas

- **Python**: Linguagem principal do projeto.
- **PLY (Python Lex-Yacc)**: Para a implementação do lexer e parser.
- **Groq API (https://api.groq.com/openai/v1/chat/completions)**: Usada para integrar recursos de inteligência artificial ao terminal, permitindo que comandos específicos sejam processados via modelo de linguagem hospedado na Groq.

## Gramática do TermIA

A gramática abaixo descreve a estrutura completa dos comandos aceitos pelo seu terminal, conforme a implementação final do parser PLY.

### Visão Geral
```text
program      := stmt_list
stmt_list    := stmt | stmt_list ';' stmt
stmt         := os_cmd | ia_cmd | meta_cmd
```

### 🧱 OS Commands
Comandos genéricos (não reservados), aceitam argumentos opcionais.
```text
os_cmd       := IDENT args_opt
args_opt     := args | empty
args         := arg | args arg
arg          := IDENT | STRING | PATH
```

### 🤖 IA Commands
```text
os_cmd       := IDENT args_opt
args_opt     := args | empty
args         := arg | args arg
arg          := IDENT | STRING | PATH
```
Esses comandos são tratados como:
```text
('ia_cmd', 'ia', SUBCOMMAND, VALUE)
```

### 🏠 Meta Commands (Comandos Internos)
```text
meta_cmd     := 'cd' PATH
              | 'pwd'
              | 'history'
              | 'ls'
              | 'ls' PATH
              | 'touch' PATH
              | 'touch' FILENAME
              | 'rm' PATH
              | 'rm' FILENAME
              | 'cat' PATH
              | 'cat' FILENAME
              | 'echo' STRING '>'  PATH
              | 'echo' STRING '>'  FILENAME
              | 'echo' STRING '>>' PATH
              | 'echo' STRING '>>' FILENAME
              | 'mkdir' PATH
              | 'mkdir' IDENT
              | 'rmdir' PATH
              | 'rmdir' IDENT
              | 'cp' PATH PATH
              | 'cp' FILENAME FILENAME
              | 'cp' FILENAME PATH
              | 'cp' PATH FILENAME
              | 'mv' PATH PATH
              | 'mv' FILENAME FILENAME
              | 'mv' FILENAME PATH
              | 'mv' PATH FILENAME
              | 'whoami'
              | 'date'
              | 'clear'
              | 'exit'
```

Esses comandos são tratados como:
```text
('meta_cmd', <nome>, [args...])
```
 
### 📁 Tipos Léxicos

#### STRING
```text
"qualquer texto com escapes \" e \\ permitido"
```
#### PATH
Caminhos com pelo menos uma / ou prefixos ./ e ../:
```text
./dir/sub/
../outro/arquivo
/home/user/docs
```
#### FILENAME
Obrigatoriamente contém extensão:
```text
arquivo.txt
dir/sub/teste.py
./local/arq.json
```

#### IDENT
Identificadores simples e comandos não reservados:
```text
run
deploy
meucomando
```
Se coincidir com uma palavra reservada (ex: cd, ls, ia, ask), vira token especial.

## 🏗️ Funcionamento e Arquitetura
O TermIA segue a arquitetura clássica de um interpretador: cada comando digitado passa pelo lexer e pelo parser (implementados com PLY), que geram uma estrutura sintática (AST). Essa estrutura é então encaminhada para o componente responsável pela execução:

- MetaCmdHandler: executa comandos internos do terminal (como cd, ls, touch, history, etc.), implementados totalmente em Python.

- IACmdHandler: lida com comandos iniciados por ia, enviando solicitações ao GroqAIService, que realiza a chamada HTTP para a API da Groq e retorna a resposta da IA.

- OS Commands: comandos genéricos (não reservados) são interpretados como chamadas de execução normal de shell.

O loop principal (main.py) integra tudo isso: lê o input, envia ao parser, identifica o tipo de comando e invoca o handler adequado. Essa arquitetura separa parsing, lógica de execução e integração com IA, permitindo extensões simples e organização modular.

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

### 🔑 Configurando o Token da Groq APIs

Para que os comandos de IA do TermIA funcionem, você precisa configurar o token da Groq API no arquivo groq_ai_service.py.

Abra o arquivo e localize:
```python
class GroqAIService:
    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    TOKEN = ""
```
Substitua "" pelo seu token da Groq:
```python
TOKEN = "gsk_seu_token_aqui"
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
