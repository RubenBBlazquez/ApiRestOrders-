FROM python:3.10
LABEL authors="rbblazquez"

WORKDIR /app

COPY requirements.txt .

RUN apt-get update -y
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get install default-mysql-client -y

COPY .. .

EXPOSE 8000
