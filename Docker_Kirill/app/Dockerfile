FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /data/images && \
    echo "Начальная информация" > /data/info.txt && \
    echo "Не обновлялось" > /data/last_update.txt

COPY default.jpg /data/images/default.jpg

EXPOSE 5000

CMD ["python", "app.py"]