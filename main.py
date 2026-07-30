import uvicorn
from fastapi import FastAPI, Body, HTTPException, status
from translator import GigaTranslator
from pydantic import BaseModel, Field
from typing import Annotated
import os
from dotenv import load_dotenv

load_dotenv()


class TranslateRequest(BaseModel):
    text_content: Annotated[str, Field(min_length=2, max_length=1000)]

app = FastAPI()

@app.post("/translate", tags=["Перевод"], summary="Перевести текст с русского языка на английский при помощи модели GigaChat")
async def eng_to_ru(translateRequest: Annotated[TranslateRequest, Body()]):
    translator = GigaTranslator(credentials=os.getenv("GIGA_CHAT_AUTH_KEY"))
    try:
        response = await translator.translate(text=translateRequest.text_content)
        return {
            "message": response
        }

    except Exception as e:
        print("Сообщение в лог")
        print(f"Перевод: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)

