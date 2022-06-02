FROM python:3.7-alpine
# RUN mkdir /backend
# WORKDIR /backend
WORKDIR .

RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
# COPY requirements.txt /backend/requirements.txt
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install grpcio-tools
RUN pip install -r requirements.txt

EXPOSE 5001

COPY . .
CMD ["flask", "run", "--host", "0.0.0.0", "--port" , "5001" ]