FROM python:3.7-alpine
# RUN mkdir /kafka_backend
# WORKDIR /kafka_backend

WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
# COPY requirements.txt /kafka_backend/requirements.txt
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "-m", "kafka_consumer.py"]
