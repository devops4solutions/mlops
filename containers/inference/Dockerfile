FROM python:3.11-slim

WORKDIR /opt/program

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY inference.py .

ENV PORT=8080
EXPOSE 8080

CMD ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "8080"]
