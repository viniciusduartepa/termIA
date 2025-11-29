# completion.py
import os
import glob
import readline
from typing import Iterable, List


def build_default_commands() -> List[str]:
    META_COMMANDS = [
        'cd', 'pwd', 'history', 'ls', 'touch', 'rm', 'cat',
        'echo', 'mkdir', 'rmdir', 'cp', 'mv',
        'whoami', 'date', 'clear', 'exit',
    ]

    IA_COMMANDS = [
        'ia', 'ask', 'summarize', 'codeexplain', 'translate', 'doc',
    ]

    OTHER_COMMANDS: List[str] = []

    return META_COMMANDS + IA_COMMANDS + OTHER_COMMANDS


def make_completer(commands: Iterable[str]):
    commands = list(commands)
    IA_SUBCOMMANDS = ['ask', 'summarize', 'codeexplain', 'translate', 'doc']

    def completer(text: str, state: int):
        buffer = readline.get_line_buffer()
        line = buffer.lstrip()
        parts = line.split()

        matches: list[str] = []

        if not parts:
            # linha vazia → completar comando
            matches = [cmd for cmd in commands if cmd.startswith(text)]
        else:
            first = parts[0]

            # completando o primeiro token (comando)
            if len(parts) == 1 and not buffer.endswith(' '):
                matches = [cmd for cmd in commands if cmd.startswith(text)]

            # depois de "ia " → completar subcomandos IA
            elif first == 'ia':
                matches = [sub for sub in IA_SUBCOMMANDS if sub.startswith(text)]

            else:
                # completar arquivo/caminho
                pattern = text + '*' if text else '*'
                paths = glob.glob(pattern)

                def decorate(path: str) -> str:
                    return path + '/' if os.path.isdir(path) else path

                matches = [decorate(m) for m in paths]

        try:
            return matches[state]
        except IndexError:
            return None

    return completer


def setup_readline(commands: Iterable[str] | None = None):
    """
    Configura o readline com:
    - completer baseado nos comandos
    - Tab como tecla de autocomplete (macOS/libedit + GNU readline)
    """
    if commands is None:
        commands = build_default_commands()

    completer = make_completer(commands)
    readline.set_completer(completer)

    # IMPORTANTE: macOS costuma usar libedit, não GNU readline
    doc = readline.__doc__ or ""
    if "libedit" in doc:
        # Sintaxe especial do libedit (macOS)
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        # GNU readline (Linux, Python via Homebrew etc.)
        readline.parse_and_bind("tab: complete")
