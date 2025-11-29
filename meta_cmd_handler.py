import os


class MetaCmdHandler:
    def __init__(self):
        self.history = []

    def add_to_history(self, line: str):
        self.history.append(line)

    def handle(self, node):
        if not node or node[0] != 'meta_cmd':
            return None

        cmd = node[1]

        if cmd == 'cd':
            path = node[2]
            return self._cd(path)

        if cmd == 'pwd':
            return self._pwd()

        if cmd == 'history':
            return self._history()

        if cmd == 'ls':
        
            path = node[2] if len(node) > 2 else '.'
            return self._ls(path)

        if cmd == 'touch':
            filename = node[2]
            return self._touch(filename)

        if cmd == 'rm':
            filename = node[2]
            return self._rm(filename)

        if cmd == 'cat':
            filename = node[2]
            return self._cat(filename)

        if cmd == 'echo':
            text = node[2]
            mode = node[3]  
            filename = node[4]
            return self._echo(text, mode, filename)
        
        if cmd == 'mkdir':
            path = node[2]
            return self._mkdir(path)

        if cmd == 'rmdir':
            path = node[2]
            return self._rmdir(path)
    
        if cmd == 'cp':
            src = node[2]
            dst = node[3]
            return self._cp(src, dst)

        if cmd == 'mv':
            src = node[2]
            dst = node[3]
            return self._mv(src, dst)

        if cmd == 'whoami':
            return self._whoami()

        if cmd == 'date':
            return self._date()

        if cmd == 'clear':
            return self._clear()

        if cmd == 'exit':
            self._exit()
            return None


        return f"Comando meta desconhecido: {cmd}"


    def _cd(self, path: str):
        try:
            os.chdir(path)
            return f"Diretório atual: {os.getcwd()}"
        except FileNotFoundError:
            return f"Diretório não encontrado: {path}"
        except NotADirectoryError:
            return f"Não é um diretório: {path}"
        except PermissionError:
            return f"Permissão negada: {path}"

    def _pwd(self):
        return os.getcwd()

    def _history(self):
        if not self.history:
            return "(histórico vazio)"

        lines = []
        for i, cmd in enumerate(self.history, start=1):
            lines.append(f"{i}: {cmd}")
        return "\n".join(lines)

    def _ls(self, path: str = '.'):
        try:
            entries = os.listdir(path)
        except FileNotFoundError:
            return f"Diretório não encontrado: {path}"
        except NotADirectoryError:
            return f"Não é um diretório: {path}"
        except PermissionError:
            return f"Permissão negada: {path}"

        dirs = []
        files = []
        for name in entries:
            full = os.path.join(path, name)
            if os.path.isdir(full):
                dirs.append(name + "/")
            else:
                files.append(name)

        dirs.sort()
        files.sort()
        return " ".join(dirs + files)



    def _touch(self, filename: str):
        try:
            with open(filename, 'a', encoding='utf-8'):
                pass
            return f"Arquivo criado: {filename}"
        except IsADirectoryError:
            return f"Não é um arquivo: {filename}"
        except PermissionError:
            return f"Permissão negada: {filename}"
        except OSError as e:
            return f"Erro ao criar arquivo '{filename}': {e}"

    def _rm(self, filename: str):
        try:
            os.remove(filename)
            return f"Arquivo removido: {filename}"
        except FileNotFoundError:
            return f"Arquivo não encontrado: {filename}"
        except IsADirectoryError:
            return f"Não é um arquivo (talvez seja diretório?): {filename}"
        except PermissionError:
            return f"Permissão negada: {filename}"
        except OSError as e:
            return f"Erro ao remover arquivo '{filename}': {e}"

    def _cat(self, filename: str):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return f"Arquivo não encontrado: {filename}"
        except IsADirectoryError:
            return f"Não é um arquivo: {filename}"
        except PermissionError:
            return f"Permissão negada: {filename}"
        except OSError as e:
            return f"Erro ao ler arquivo '{filename}': {e}"

    def _echo(self, text: str, mode: str, filename: str):
        if len(text) >= 2 and text[0] == '"' and text[-1] == '"':
            text_content = text[1:-1]
        else:
            text_content = text

        file_mode = 'w' if mode == 'write' else 'a'
        try:
            with open(filename, file_mode, encoding='utf-8') as f:
                f.write(text_content + "\n")
            acao = "sobrescrito" if file_mode == 'w' else "adicionado"
            return f"Texto {acao} em: {filename}"
        except IsADirectoryError:
            return f"Não é um arquivo: {filename}"
        except PermissionError:
            return f"Permissão negada: {filename}"
        except OSError as e:
            return f"Erro ao escrever em '{filename}': {e}"
        
    def _mkdir(self, path: str):
        try:
            os.mkdir(path)
            return f"Diretório criado: {path}"
        except FileExistsError:
            return f"Já existe arquivo ou diretório com esse nome: {path}"
        except PermissionError:
            return f"Permissão negada: {path}"
        except OSError as e:
            return f"Erro ao criar diretório '{path}': {e}"

    def _rmdir(self, path: str):
        try:
            os.rmdir(path)
            return f"Diretório removido: {path}"
        except FileNotFoundError:
            return f"Diretório não encontrado: {path}"
        except NotADirectoryError:
            return f"Não é um diretório: {path}"
        except OSError as e:
            return f"Erro ao remover diretório '{path}': {e}"
    
    def _cp(self, src: str, dst: str):
        import shutil
        try:
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            return f"Copiado: {src} → {dst}"
        except FileNotFoundError:
            return f"Arquivo/Diretório não encontrado: {src}"
        except FileExistsError:
            return f"Destino já existe: {dst}"
        except PermissionError:
            return f"Permissão negada: {src}"
        except OSError as e:
            return f"Erro ao copiar '{src}' para '{dst}': {e}"

    def _mv(self, src: str, dst: str):
        import shutil
        try:
            shutil.move(src, dst)
            return f"Movido: {src} → {dst}"
        except FileNotFoundError:
            return f"Arquivo/Diretório não encontrado: {src}"
        except PermissionError:
            return f"Permissão negada: {src}"
        except OSError as e:
            return f"Erro ao mover '{src}' para '{dst}': {e}"
    
    def _whoami(self):
        import getpass
        try:
            return getpass.getuser()
        except Exception as e:
            return f"Erro ao obter usuário: {e}"

    def _date(self):
        from datetime import datetime
        try:
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            return f"Erro ao obter data/hora: {e}"
    
    def _clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
       
        return None

    def _exit(self):
        raise SystemExit


