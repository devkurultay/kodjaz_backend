source .env
cd code_runner/

docker build -t $AWS_ECR_PYTHON_REPO_NAME:v2 .