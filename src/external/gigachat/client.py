import uuid
import ssl
import httpx
from src.config.project_config import settings


class GigaChatClient:
    def __init__(self):
        self.auth_key = settings.gigachat.auth_key
        self.model = settings.gigachat.model
        self.scope = settings.gigachat.scope
        self.max_tokens = settings.gigachat.max_tokens
        self.temperature = settings.gigachat.temperature

        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    async def _get_token(self, client: httpx.AsyncClient) -> str:
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
            "Authorization": f"Basic {self.auth_key}"
        }
        data = {"scope": self.scope}
        response = await client.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()["access_token"]

    async def chat_completion(self, messages: list[dict]) -> str:
        async with httpx.AsyncClient(verify=self.ssl_context, timeout=30.0) as client:
            token = await self._get_token(client)
            url = "https://api.giga.chat/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]