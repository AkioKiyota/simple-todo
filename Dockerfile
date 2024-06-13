
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /django

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt