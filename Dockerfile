FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production
ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV DEBUG=False
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["python", "-m", "src.api"]
