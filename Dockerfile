FROM python:3.9.13-alpine

WORKDIR /app

RUN pip install loguru python-telegram-bot requests

COPY src ./src

CMD ["python3", "src/main.py"]
