FROM python:3.10-slim

WORKDIR /app


RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY requirements.txt .

RUN echo "hi"
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
