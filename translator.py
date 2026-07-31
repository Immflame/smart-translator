import uuid
import ssl
import httpx
from enum import Enum


class GigaTranslator:
    def __init__(self,
                 credentials: str,
                 model: str = "GigaChat-2-Max",
                 scope: str = "GIGACHAT_API_PERS"
                 ):
        self.credentials = credentials
        self.model = model
        self.scope = scope

        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    def _get_language_name(self, lang_code: str) -> str:
        lang_names = {
            "rus": "русский",
            "eng": "английский",
            "spa": "испанский",
            "fre": "французский",
            "ger": "немецкий",
            "ita": "итальянский",
            "chi": "китайский",
            "ara": "арабский",
            "por": "португальский",
            "jpn": "японский",
            "kor": "корейский",
            "hin": "хинди",
            "tur": "турецкий",
            "ukr": "украинский",
            "pol": "польский",
            "dut": "голландский",
            "vie": "вьетнамский",
            "tha": "тайский",
            "ind": "индонезийский",
            "heb": "иврит",
            "per": "персидский"
        }
        return lang_names.get(lang_code, lang_code)

    def _get_system_prompt(self, source_lang: str, target_lang: str) -> str:
        source_name = self._get_language_name(source_lang)
        target_name = self._get_language_name(target_lang)

        return (
            f"Ты - профессиональный переводчик, специализирующийся на переводе с {source_name} на {target_name} язык.\n\n"
            f"Твоя задача - точно и качественно перевести предоставленный текст с {source_name} на {target_name}, сохраняя его смысл, стиль и структуру.\n\n"
            "### Инструкция по переводу:\n\n"
            "1. Внимательно прочитай весь текст перед началом перевода.\n"
            "2. Переводи предложение за предложением, сохраняя оригинальную структуру абзацев.\n"
            "3. Строго соблюдай следующие правила:\n"
            "   - Полностью сохраняй смысл и стилистику оригинала.\n"
            "   - Не переводи нетекстовые элементы (коды программ, математические формулы, технические обозначения). Оставляй их в оригинальном виде.\n"
            "   - Имена собственные, географические названия, бренды оставляй без перевода, транслитерируя их согласно правилам целевого языка, если необходимо.\n"
            "   - При встрече со специализированной терминологией используй общепринятые эквиваленты на целевом языке.\n"
            "   - Идиомы и устойчивые выражения переводи соответствующими аналогами на целевом языке, а не дословно.\n"
            "4. Если встретишь двусмысленные фразы или слова с несколькими значениями, выбирай наиболее подходящий вариант исходя из контекста всего документа.\n"
            "5. Обеспечь грамматическую корректность и естественность звучания перевода на целевом языке.\n\n"
            "### Формат ответа:\n"
            "Предоставь только итоговый переведенный текст на целевом языке. Не добавляй никаких комментариев, объяснений или дополнительной информации.\n\n"
            "### Примечания:\n"
            "- Если какой-либо фрагмент текста невозможно однозначно перевести из-за отсутствия контекста, сохрани его максимально близко к оригиналу.\n"
            "## Критерии качества:\n"
            "- Точность передачи смысла оригинала\n"
            "- Естественность и грамотность текста на целевом языке\n"
            "- Соответствие стилю исходного материала\n"
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

    async def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        if not text or not text.strip():
            return "Ошибка: Текст не может быть пустым"

        system_prompt = self._get_system_prompt(source_lang, target_lang)

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
                        {"role": "system", "content": system_prompt},
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