FROM python:3.11-slim
FROM python:aaa

WORKDIR /app

COPY . .

RUN pip install pytest ruff

CMD ["python"]