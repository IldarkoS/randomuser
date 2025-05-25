FROM python:3.11-slim

WORKDIR /app

COPY test_requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && pip install -r test_requirements.txt

COPY ../ .

ENV PYTHONPATH=/app

CMD ["pytest", "-v"]