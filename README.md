Local

docker build -t ml-train:latest -f Dockerfile.train .
docker run --rm -v "$PWD/artifacts:/app/artifacts" ml-train:latest

docker build -t ml-serve:latest -f Dockerfile.serve .

docker run --rm -p 8080:8080 -v "$PWD/artifacts:/app/artifacts" ml-serve:latest


curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [
      14.0,20.0,90.0,600.0,0.10,0.12,0.10,0.05,0.18,0.06,
      0.40,1.20,2.50,40.0,0.01,0.02,0.02,0.01,0.02,0.003,
      16.0,28.0,110.0,900.0,0.14,0.30,0.25,0.12,0.28,0.08
    ]
  }'
