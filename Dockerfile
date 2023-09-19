FROM python:3.11-slim

ENV PYTHONWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /app/src/

COPY . .

RUN pip install -r requirements.txt
CMD ["python3", "main.py"]
