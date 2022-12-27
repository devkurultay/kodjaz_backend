#!make
include .env

ACTIVATE := . env/bin/activate

venv:
	test -d env || python3 -m venv env && chmod +x env/bin/activate

install: venv
	$(ACTIVATE) && pip install --upgrade pip && pip install -r requirements/requirements_dev.txt

test:
	$(ACTIVATE) && python manage.py test $(word 2,$(MAKECMDGOALS))

makemigrations:
	$(ACTIVATE) && python manage.py makemigrations

migrate:
	$(ACTIVATE) && python manage.py migrate

run:
	$(ACTIVATE) && python manage.py runserver

runreact:
	cd frontend && REACT_APP_BASE_URL=http://localhost:8000/api/ npm run start

buildreact-dev:
	cd frontend && REACT_APP_BASE_URL=http://localhost:8000/api/ npm run build

buildreact-prod:
	cd frontend && REACT_APP_BASE_URL=https://backend.kodjaz.com/api/ npm run build

buildcoderunner:
	cd code_runner && docker build -t $(AWS_ECR_PYTHON_REPO_NAME):latest .

.PHONY: pushdocker

pushdocker:
	cd code_runner/
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com
	docker tag $(AWS_ECR_PYTHON_REPO_NAME):latest $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(AWS_ECR_PYTHON_REPO_NAME):latest
	docker push $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(AWS_ECR_PYTHON_REPO_NAME):latest

deploy: buildreact-prod
	./deploy_to_server.sh