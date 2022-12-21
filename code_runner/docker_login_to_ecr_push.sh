source .env
cd code_runner/

# Log in to AWS
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Put a tag
docker tag $AWS_ECR_PYTHON_REPO_NAME:v2 $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$AWS_ECR_PYTHON_REPO_NAME:v2
# Push to AWS ECR
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$AWS_ECR_PYTHON_REPO_NAME:v2