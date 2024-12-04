FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r req.txt

COPY . .
CMD ["python", "main.py"]