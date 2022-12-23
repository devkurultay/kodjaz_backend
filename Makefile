#!make
include .env

runserver:
	python manage.py runserver

test:
	python manage.py test

runreact:
	cd frontend && REACT_APP_BASE_URL=http://localhost:8000/api/ npm run start

buildreact-dev:
	cd frontend && REACT_APP_BASE_URL=http://localhost:8000/api/ npm run build

buildreact-prod:
	cd frontend && npm run build

buildcoderunner:
	cd code_runner && docker build -t $(AWS_ECR_PYTHON_REPO_NAME):v2 .

.PHONY: pushdocker

pushdocker:
	cd code_runner/
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com
	docker tag $(AWS_ECR_PYTHON_REPO_NAME):v2 $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(AWS_ECR_PYTHON_REPO_NAME):v2
	docker push $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(AWS_ECR_PYTHON_REPO_NAME):v2
