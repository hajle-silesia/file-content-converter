FROM python:3.9-slim
RUN apt update && apt install -y \
    curl
WORKDIR app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app/src .
ENTRYPOINT ["python", "main.py"]