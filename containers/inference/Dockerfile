FROM python:3.11-slim

WORKDIR /opt/program

RUN pip install --no-cache-dir fastapi uvicorn joblib scikit-learn pydantic

COPY inference.py /opt/program/inference.py
COPY serve_entrypoint.py /opt/program/serve_entrypoint.py

EXPOSE 8080

ENTRYPOINT ["python", "/opt/program/serve_entrypoint.py"]
CMD ["serve"]