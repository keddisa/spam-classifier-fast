Start virtual environment
python3 -m venv spam-classifier-api //creates the spam-classifier-api directory
source spam-classifier-api/bin/activate



installation
pip3 install fastapi
pip3 install uvicorn

if there is a requirements.txt file:

pip install -r requirements.txt

run the server:
uvicorn main:app --reload



# Build the Docker image
docker build -t fastapi-app .

# Authenticate Docker to the ECR registry
aws ecr get-login-password | docker login --username AWS --password-stdin 529633373274.dkr.ecr.us-east-1.amazonaws.com/spam-classifier-fast

# Tag your Docker image with the ECR repository URI
docker tag spam-classifier-fast:latest 529633373274.dkr.ecr.us-east-1.amazonaws.com/spam-classifier-fast:latest

# Push the Docker image to ECR
docker push 529633373274.dkr.ecr.us-east-1.amazonaws.com/spam-classifier-fast:latest



## FROM EC2 Instance
# Authenticate Docker to the ECR registry
aws ecr get-login-password | docker login --username AWS --password-stdin 529633373274.dkr.ecr.us-east-1.amazonaws.com/spam-classifier-fast

# Pull the Docker image from ECR
docker pull 529633373274.dkr.ecr.us-east-1.amazonaws.com/spam-classifier-fast:latest

# Run the FastAPI Docker container
docker run -d -p 80:80 529633373274.dkr.ecr.us-east-1.amazonaws.com/spam-classifier-fast:latest

