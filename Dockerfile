FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y netcat-openbsd

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV FLASK_APP=run.py
ENV FLASK_RUN_PORT=5000

RUN chmod +x entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]