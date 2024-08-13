from fastapi import FastAPI, File, Query, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from .openai_whisper.openai_whisper import whisper_generate, LANGUAGE_CODES
from fastapi.responses import StreamingResponse
from typing import Union, List
from .kimi.kimi import kimi_generate

app = FastAPI()


@app.get("/", response_class=RedirectResponse)
async def root():
    return "/docs"


@app.post("/kimi/")
async def kimi_handler():
    return StreamingResponse(kimi_generate(), media_type='text/event-stream')


@app.post("openai_whisper/")
async def whisper_handler(
        files: List[UploadFile] = File([]),
        url: Union[str, None] = Query(default=None),
        uid: Union[str, None] = Query(default=None),
        language: Union[str, None] = Query(default=None, enum=LANGUAGE_CODES),
):
    print("openai_whisper started", language, url)
    return JSONResponse(content={"data": whisper_generate(files, url, uid, language)})
