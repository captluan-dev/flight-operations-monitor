FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY collector/collector.py collector/flight_api.py ./collector/

WORKDIR /app/collector
CMD ["python", "collector.py"]