FROM python:3.9-slim-buster

RUN pip install uv

WORKDIR /app

COPY . .

CMD ["uv", "run", "index.py"]