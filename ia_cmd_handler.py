import os
from groq_ai_service import GroqAIService


class IACmdHandler:
    def __init__(self, logger=None):
        self.logger = logger or (lambda msg: print(f"[IA-LOG] {msg}"))
        self.ai = GroqAIService()

    def handle(self, node):
        if not node or node[0] != 'ia_cmd':
            return None

        _, _, command, payload = node


        if isinstance(payload, str) and payload.startswith('"') and payload.endswith('"'):
            payload = payload[1:-1]

        cmd = str(command).lower()

        if cmd == 'ask':
            return self._handle_ask(payload)

        elif cmd == 'summarize':
            return self._handle_summarize(payload)

        elif cmd == 'codeexplain':
            return self._handle_codeexplain(payload)

        elif cmd == 'translate':        
            return self._handle_translate(payload)

        elif cmd == 'doc':             
            return self._handle_doc(payload)

        else:
            return f"Comando IA desconhecido: {command}"


    # -----------------------------
    # Handlers internos
    # -----------------------------

    def _handle_ask(self, payload: str):
        prompt = f"responda: {payload}"
        return self.ai.send(prompt)

    def _handle_summarize(self, payload: str):
        prompt = f"resuma: {payload}"
        return self.ai.send(prompt)

    def _handle_codeexplain(self, filename: str):

        if not os.path.exists(filename):
            return f"Erro: arquivo '{filename}' não encontrado."

        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        prompt = f"explique o código:\n\n{content}"
        return self.ai.send(prompt)
    
    def _handle_translate(self, payload: str):
        prompt = (
            "Traduza o texto abaixo para português do Brasil, "
            f"{payload}"
        )
        return self.ai.send(prompt)

    def _handle_doc(self, filename: str):

        if not os.path.exists(filename):
            return f"Erro: arquivo '{filename}' não encontrado."

        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        prompt = (
            "Gere uma documentação técnica clara e organizada para o código a seguir.\n"
            "- Explique o propósito geral do arquivo.\n"
            "- Liste e documente as principais funções / classes.\n"
            "- Descreva brevemente parâmetros e retornos.\n"
            "- Use português do Brasil.\n\n"
            f"{content}"
        )
        return self.ai.send(prompt)