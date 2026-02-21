# Local

docker build -t ml-train:latest -f Dockerfile .
docker run --rm -v "$PWD/artifacts:/app/artifacts" ml-train:latest

docker build -t ml-serve:latest -f Dockerfile .

docker run --rm -p 8080:8080 -v "$PWD/artifacts:/app/artifacts" ml-serve:latest

docker run --rm -p 8080:8080 \
  -v "$PWD/artifacts:/opt/ml/model" \
   inference:latest serve

curl -i http://localhost:8080/ping

curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"features":[14.0,20.0,90.0,600.0,0.10,0.12,0.10,0.05,0.18,0.06,0.40,1.20,2.50,40.0,0.01,0.02,0.02,0.01,0.02,0.003,16.0,28.0,110.0,900.0,0.14,0.30,0.25,0.12,0.28,0.08]}'



curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [
      14.0,20.0,90.0,600.0,0.10,0.12,0.10,0.05,0.18,0.06,
      0.40,1.20,2.50,40.0,0.01,0.02,0.02,0.01,0.02,0.003,
      16.0,28.0,110.0,900.0,0.14,0.30,0.25,0.12,0.28,0.08
    ]
  }'


# Train a job
ECR private repo is required for sagemaker
echo "dummy" > dummy.txt
aws s3 cp dummy.txt s3://mlops-devops4solutions/training-input/dummy.txt
 aws sagemaker create-training-job --cli-input-json file://train-job.json 

 aws sagemaker create-model \                   
  --cli-input-json file://create-model.json \
  --region us-east-1
aws sagemaker create-endpoint-config \
  --cli-input-json file://endpoint-config.json \
  --region us-east-1

  aws sagemaker create-endpoint \
  --cli-input-json file://endpoint.json \
  --region us-east-1

aws sagemaker describe-endpoint \
  --endpoint-name mlops-demo-endpoint-002 \
  --region us-east-1

 An error occurred (ValidationException) when calling the CreateModel operation: Unsupported manifest media type application/vnd.oci.image.index.v1+json for image 936379345511.dkr.ecr.us-east-1.amazonaws.com/mlops-train:latest. Ensure that valid manifest media type is used for specified image.
 update the workflow                                   


 aws sagemaker-runtime invoke-endpoint \
  --endpoint-name mlops-demo-endpoint-002 \
  --content-type application/json \
  --body fileb://payload.json \
  out.json \
  --region us-east-1

cat out.json


aws sagemaker delete-endpoint --endpoint-name mlops-demo-endpoint-002 --region us-east-1
aws sagemaker delete-endpoint-config --endpoint-config-name mlops-demo-epc-002 --region us-east-1
aws sagemaker delete-model --model-name mlops-demo-model-002 --region us-east-1

  "EndpointStatus": "Failed",
    "FailureReason": "CannotStartContainerError. Please ensure the model container for variant AllTraffic starts correctly when invoked with 'docker run <image> serve'",

# Put a real model.joblib in ./tmp_model/model.joblib for test
mkdir -p tmp_model
# (copy your model.joblib from extracted model.tar.gz into tmp_model)

Local testing


### Create a Model Registry
aws sagemaker create-model-package-group \
  --model-package-group-name mlops-demo-group \
  --model-package-group-description "MLOps demo model registry" \
  --region us-east-1

aws sagemaker create-model-package \
  --cli-input-json file://register-model.json \
  --region us-east-1