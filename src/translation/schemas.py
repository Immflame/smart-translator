from pydantic import BaseModel, Field
from typing import Annotated
from enum import Enum


class SupportedLanguages(str, Enum):
    """ коды языков """
    RUS = "rus"
    ENG = "eng"
    SPA = "spa"
    FRE = "fre"
    GER = "ger"
    CHI = "chi"
    ARA = "ara"
    POR = "por"
    ITA = "ita"
    JPN = "jpn"


class TranslateRequest(BaseModel):
    """ запрос на перевод текста """
    source_lang: SupportedLanguages
    target_lang: SupportedLanguages
    content: Annotated[str, Field(min_length=1, max_length=2000)]


class TranslateResponse(BaseModel):
    """ переведенный текст """
    message: str
