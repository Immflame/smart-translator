from src.external.gigachat.client import GigaChatClient
from constants import LANGUAGE_NAMES
from exceptions import TranslationError


class TranslationService:
    def __init__(self, gigachat_client: GigaChatClient):
        self.gigachat_client = gigachat_client

    def _get_system_prompt(self, source_lang: str, target_lang: str) -> str:
        source_name = LANGUAGE_NAMES.get(source_lang, source_lang)
        target_name = LANGUAGE_NAMES.get(target_lang, target_lang)
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

    async def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        if not text or not text.strip():
            raise TranslationError("Текст не может быть пустым")

        system_prompt = self._get_system_prompt(source_lang, target_lang)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]

        try:
            return await self.gigachat_client.chat_completion(messages)
        except Exception as e:
            raise TranslationError(f"Ошибка перевода: {str(e)}")
