FROM python:latest

WORKDIR /app

COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt -U

COPY memory_info.py .

RUN mkdir -p data

ENTRYPOINT ["python3", "memory_info.py"]
