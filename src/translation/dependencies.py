from fastapi import Depends
from src.external.gigachat.client import GigaChatClient
from service import TranslationService


def get_gigachat_client() -> GigaChatClient:
    return GigaChatClient()


def get_translation_service(
    client: GigaChatClient = Depends(get_gigachat_client)
) -> TranslationService:
    return TranslationService(gigachat_client=client)
