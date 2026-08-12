FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
COPY app.py app.py
COPY src src

EXPOSE 3002

CMD ["uvicorn", "app:app",  "--host",  "0.0.0.0", "--port", "3002", "--log-level", "debug"]