import uuid
import ssl
import httpx


class GigaTranslator:
    def __init__(self, credentials: str, model: str = "GigaChat-2-Max", scope: str = "GIGACHAT_API_PERS"):
        self.credentials = credentials
        self.model = model
        self.scope = scope

        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

        self.system_prompt = ("Ты - профессиональный переводчик на русский язык.\n"
                              "## Задача: перевести оригинальный текст на русский язык\n"
                              "## Правила:\n"
                              "- Все нетекстовые фрагменты (код, формулы и т.д.) переводить не нужно.\n"
                              "- Орфографические и пунктуационные ошибки исправлять не нужно.\n"
                              "## Формат ответа:\n"
                              "Твой ответ должен содержать только переведенный текст. Никаких пояснений."
                              )

    async def _get_token(self, client: httpx.AsyncClient) -> str:
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
            "Authorization": f"Basic {self.credentials}"
        }
        data = {"scope": self.scope}

        response = await client.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()["access_token"]

    async def translate(self, text: str) -> str:
        if not text or not text.strip():
            return "Ошибка: Текст не может быть пустым"

        async with httpx.AsyncClient(verify=self.ssl_context, timeout=30.0) as client:
            try:
                token = await self._get_token(client)

                url = "https://api.giga.chat/v1/chat/completions"
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {token}"
                }

                payload = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": text}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 1024
                }

                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()

                return response.json()["choices"][0]["message"]["content"]
            except Exception as e:
                return f"Ошибка перевода: {str(e)}"