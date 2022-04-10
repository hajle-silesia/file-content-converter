import os

from fastapi import FastAPI

from file_content_converter import FileContentConverter


api = FastAPI()
host = os.getenv('FILE_CONTENT_MONITOR_SERVICE_HOST')
port = os.getenv('FILE_CONTENT_MONITOR_SERVICE_PORT')
url = f"http://{host}:{port}/content"
file_content_converter = FileContentConverter(url)


@api.get("/content")
async def content():
    return {"content": file_content_converter.content,
            }
