from fastapi import Depends
from ..external.gigachat import client
from .service import TranslationService


def get_gigachat_client() -> client.GigaChatClient:
    return client.GigaChatClient()


def get_translation_service(
    client: client.GigaChatClient = Depends(get_gigachat_client)
) -> TranslationService:
    return TranslationService(gigachat_client=client)
