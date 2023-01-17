#!make
include .env

.PHONY: clearstatic pushdocker buildreact-dev buildreact-prod run-build-collect-static-prod deploy

PROD_API_URL_ROOT := https://$(BACKEND_URL_ROOT)/api/
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
	cd frontend && REACT_APP_BASE_URL=$(API_URL_ROOT) npm run start

clearstatic:
	rm -rf staticfiles/

buildreact-dev:
	cd frontend && REACT_APP_BASE_URL=$(API_URL_ROOT) npm run build
	$(ACTIVATE) && python manage.py collectstatic --noinput

buildreact-prod:
	cd frontend && REACT_APP_BASE_URL=$(PROD_API_URL_ROOT) npm run build

run-build-collect-static-prod: buildreact-prod
	$(ACTIVATE) && python manage.py collectstatic --noinput --settings=config.settings_prod

buildcoderunner:
	cd code_runner && docker build -t $(AWS_ECR_PYTHON_REPO_NAME):latest .

pushdocker:
	cd code_runner/
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com
	docker tag $(AWS_ECR_PYTHON_REPO_NAME):latest $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(AWS_ECR_PYTHON_REPO_NAME):latest
	docker push $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(AWS_ECR_PYTHON_REPO_NAME):latest

deploy: buildreact-prod
	chmod +x deploy_to_server.sh
	./deploy_to_server.sh
	$(MAKE) clearstatic

export-course:
	$(ACTIVATE) && python manage.py dumpdata courses users --exclude=courses.submission --format=json --indent=4 --output=fixtures/courses.json --natural-primary --natural-foreign
