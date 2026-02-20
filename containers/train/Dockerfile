FROM python:3.11-slim

WORKDIR /opt/ml/code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY train.py .

# SageMaker Training will run this
ENV SAGEMAKER_PROGRAM=train.py

ENTRYPOINT ["python", "train.py"]
