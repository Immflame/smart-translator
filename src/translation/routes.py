from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import TranslateRequest, TranslateResponse
from .service import TranslationService
from .dependencies import get_translation_service


router = APIRouter(prefix="/translate", tags=["Перевод"])


@router.post("", response_model=TranslateResponse)
async def translate_endpoint(
    request: TranslateRequest,
    service: TranslationService = Depends(get_translation_service)
):
    """ принимает текст, код языка с которого перевести и код языка на который перевести и возвращает ответ"""
    try:
        result = await service.translate(
            text=request.content,
            source_lang=request.source_lang.value,
            target_lang=request.target_lang.value
        )
        return TranslateResponse(message=result)
    except Exception as e:
        print(f"Ошибка в контроллере: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при переводе"
        )
