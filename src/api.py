import base64
import json
import os
import pathlib

import common.notifier
import common.storage
import fastapi
import requests

from src.file_content_converter import FileContentConverter

config_path = pathlib.Path(__file__).parent / "../file_content_converter/config.json"

app = fastapi.FastAPI()

storage = common.storage.Storage()
storage.path = config_path
notifier = common.notifier.Notifier(storage)
file_content_converter = FileContentConverter(notifier)

notifier_host = os.getenv('FILE_CONTENT_MONITOR_SERVICE_HOST')
notifier_port = os.getenv('FILE_CONTENT_MONITOR_SERVICE_PORT')
notifier_url = f"http://{notifier_host}:{notifier_port}/observers/register"

host = os.getenv('FILE_CONTENT_CONVERTER_SERVICE_HOST')
port = os.getenv('FILE_CONTENT_CONVERTER_SERVICE_PORT')
url = f"http://{host}:{port}/update"

requests.post(notifier_url, base64.b64encode(json.dumps({'file-content-converter': url}).encode()))


@app.get("/healthz")
async def healthz():
    return {'status': "ok"}


@app.get("/api")
async def api():
    return {"/content",
            "/update",
            }


@app.get("/content")
async def content():
    return {"content": file_content_converter.content,
            }


@app.get("/observers")
async def observers():
    return notifier.observers


@app.post("/observers/register")
async def observers_register(request: fastapi.Request):
    request_body_json = base64.b64decode(await request.body()).decode()
    request_body = json.loads(request_body_json)
    notifier.register_observer(request_body)


@app.post("/observers/remove")
async def observers_remove(request: fastapi.Request):
    request_body_json = base64.b64decode(await request.body()).decode()
    request_body = json.loads(request_body_json)
    notifier.remove_observer(request_body)


@app.post("/update")
async def update(request: fastapi.Request):
    request_body_json = base64.b64decode(await request.body()).decode()
    request_body = json.loads(request_body_json)
    file_content_converter.update(request_body)
