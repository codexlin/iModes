from fastapi import FastAPI, File, Query, UploadFile, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from tempfile import TemporaryDirectory
import whisper
from whisper import tokenizer
import torch
import os
from typing import Union, List
import requests

# 检查是否有NVIDIA GPU可用
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# 加载Whisper模型
model_name = os.getenv("MODEL", "large")
model = whisper.load_model(model_name, device=DEVICE)
LANGUAGE_CODES = sorted(tokenizer.LANGUAGES.keys())

app = FastAPI()
print(DEVICE, model_name)


def save_uploaded_file(upload_file: UploadFile, destination: str) -> None:
    """将上传的文件保存到指定的路径"""
    try:
        with open(destination, "wb") as out_file:
            out_file.write(upload_file.file.read())
    except PermissionError as e:
        raise HTTPException(status_code=500, detail=f"Permission denied: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")


def download_file(url: str, destination: str) -> None:
    """从URL下载文件并保存到指定路径"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(destination, "wb") as out_file:
            for chunk in response.iter_content(chunk_size=8192):
                out_file.write(chunk)
    except requests.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to download file: {str(e)}"
        )


def transcribe_file(file_path: str, language: Union[str, None]) -> dict:
    """使用Whisper模型转录文件"""
    try:
        transcribe_language = language if language is not None else None
        result = model.transcribe(file_path, language=transcribe_language)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"发生错误: {str(e)}")


@app.post("/whisper/")
async def handler(
    files: List[UploadFile] = File([]),
    url: Union[str, None] = Query(default=None),
    uid: Union[str, None] = Query(default=None),
    language: Union[str, None] = Query(default=None, enum=LANGUAGE_CODES),
):
    print("whisper started", language, url)
    if not files and not url:
        raise HTTPException(status_code=400, detail="No files or URL provided")

    results = []

    # 使用TemporaryDirectory创建临时目录
    with TemporaryDirectory() as temp_dir:
        if url:
            temp_file_path = os.path.join(temp_dir, os.path.basename(url))
            download_file(url, temp_file_path)
            result = transcribe_file(temp_file_path, language)
            results.append(
                {
                    "filename": os.path.basename(url),
                    "transcript": result["text"],
                    "language": result["language"] if language is None else language,
                }
            )

        for file in files:
            try:
                temp_file_path = os.path.join(temp_dir, file.filename)
                save_uploaded_file(file, temp_file_path)
                result = transcribe_file(temp_file_path, language)
                results.append(
                    {
                        "uid": uid,
                        "filename": file.filename,
                        "transcript": result["text"],
                        "language": result["language"]
                        if language is None
                        else language,
                    }
                )
            except HTTPException as e:
                raise e  # 重新抛出 HTTP 异常
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to process file {file.filename}: {str(e)}",
                )

    return JSONResponse(content={"data": results})


@app.get("/", response_class=RedirectResponse)
async def redirect_to_docs():
    return "/docs"
