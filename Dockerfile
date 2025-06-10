FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV FLASK_APP=run.py
ENV FLASK_RUN_PORT=5000

EXPOSE 5000

RUN chmod +x start.sh

CMD ["./start.sh"]