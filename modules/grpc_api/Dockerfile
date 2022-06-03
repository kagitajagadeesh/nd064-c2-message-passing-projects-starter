FROM python:3.7-buster
# RUN mkdir /grpc_backend
# WORKDIR /grpc_backend
WORKDIR .

# COPY requirements.txt /grpc_backend/requirements.txt

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5005

COPY . .
CMD ["python", "wsgi.py"]
