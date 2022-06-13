import base64
import json
import os

from fastapi import FastAPI, Request

from src.file_content_converter import FileContentConverter

api = FastAPI()
host = os.getenv('FRONTEND_SERVICE_HOST')
port = os.getenv('FRONTEND_SERVICE_PORT')
url = f"http://{host}:{port}/update"
file_content_converter = FileContentConverter(url)


@api.get("/api")
async def content():
    return {"/content",
            }


@api.get("/content")
async def content():
    return {"content": base64.b64encode(json.dumps(file_content_converter.content).encode()),
            }


@api.post("/update")
async def update(request: Request):
    request_body = base64.b64decode(await request.body()).decode()
    file_content_converter.update(request_body)
