import subprocess
import json
import logging

class GroqAIService:
    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    TOKEN = ""

    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='[GroqAIService] %(message)s')

    def send(self, message: str) -> str:

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": message}]
        }

        data_str = json.dumps(payload)

        curl_cmd = [
            "curl",
            "--request", "POST",
            "--url", self.API_URL,
            "--header", f"Authorization: Bearer {self.TOKEN}",
            "--header", "Content-Type: application/json",
            "--data", data_str
        ]

        result = subprocess.run(
            curl_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            logging.error(f"Erro ao chamar IA: {result.stderr}")
            return f"Erro: {result.stderr}"

        try:
            data = json.loads(result.stdout)
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            logging.error(f"Erro ao interpretar resposta: {e}")
            return result.stdout
