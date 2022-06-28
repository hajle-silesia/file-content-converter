import base64
import os

from fastapi import FastAPI, Request

from src.file_content_converter import FileContentConverter

app = FastAPI()
host = os.getenv('FRONTEND_SERVICE_HOST')
port = os.getenv('FRONTEND_SERVICE_PORT')
url = f"http://{host}:{port}/update"
file_content_converter = FileContentConverter(url)


@app.get("/api")
async def api():
    return {"/content",
            }


@app.get("/content")
async def content():
    return {"content": file_content_converter.content,
            }


@app.post("/update")
async def update(request: Request):
    request_body = base64.b64decode(await request.body()).decode()
    file_content_converter.update(request_body)
