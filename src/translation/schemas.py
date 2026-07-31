from pydantic import BaseModel, Field
from typing import Annotated
from enum import Enum


class SupportedLanguages(str, Enum):
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
    source_lang: SupportedLanguages
    target_lang: SupportedLanguages
    content: Annotated[str, Field(min_length=1, max_length=2000)]


class TranslateResponse(BaseModel):
    message: str
