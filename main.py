import uvicorn
from fastapi import FastAPI, Body, HTTPException, status
from translator import GigaTranslator
from pydantic import BaseModel, Field
from typing import Annotated
import os
from dotenv import load_dotenv
from enum import Enum

class SupportedLanguages(Enum):
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


load_dotenv()


class EngToRusRequest(BaseModel):
    text_content: Annotated[str, Field(min_length=2, max_length=1000)]

class TranslateRequest(BaseModel):
    source_lang: SupportedLanguages
    target_lang: SupportedLanguages
    content: Annotated[str, Field(min_length=1, max_length=2000)]


app = FastAPI()

@app.post("/translate/eng_to_ru", tags=["Перевод"], summary="Перевести текст с английского языка на русский при помощи модели GigaChat", deprecated=True)
async def eng_to_ru(entToRusRequest: Annotated[EngToRusRequest, Body()]):
    translator = GigaTranslator(credentials=os.getenv("GIGA_CHAT_AUTH_KEY"))
    try:
        response = await translator.translate(text=entToRusRequest.text_content)
        return {
            "message": response
        }

    except Exception as e:
        print("Сообщение в лог")
        print(f"Перевод: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@app.post("/translate", tags=["Перевод"])
async def translate(translateRequest: TranslateRequest):
    translator = GigaTranslator(credentials=os.getenv("GIGA_CHAT_AUTH_KEY"))
    try:
        response = await translator.translate(source_lang=translateRequest.source_lang,
                                              target_lang=translateRequest.target_lang,
                                              text=translateRequest.content)
        return {
            "message": response
        }

    except Exception as e:
        print("Сообщение в лог")
        print(f"Перевод: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)

