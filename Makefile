#!make
include .env

.PHONY: clearstatic collectstatic pushdocker buildreact-dev buildreact-vps-prod buildreact-zappa-prod buildreact-zappa-dev \
	collectstatic-zappa-dev collectstatic-zappa-prod replace-env-dev replace-env-prod

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

collectstatic:
	$(ACTIVATE) && python manage.py collectstatic --noinput --settings=config.settings_prod

buildreact-dev:
	cd frontend && REACT_APP_BASE_URL=$(API_URL_ROOT) npm run build
	$(ACTIVATE) && python manage.py collectstatic --noinput

buildreact-vps-prod:
	cd frontend && REACT_APP_BASE_URL=https://$(VPS_PROD_BACKEND_URL_ROOT)/api/ npm run build

buildreact-zappa-prod:
	cd frontend && REACT_APP_BASE_URL=https://$(ZAPPA_PROD_BACKEND_URL_ROOT)/api/ npm run build

buildreact-zappa-dev:
	cd frontend && REACT_APP_BASE_URL=https://$(ZAPPA_DEV_BACKEND_URL_ROOT)/api/ npm run build

collectstatic-zappa-dev: buildreact-zappa-dev
	export ENV=dev_zappa
	$(MAKE) collectstatic
	export ENV=dev_local

collectstatic-zappa-prod: buildreact-zappa-prod
	export ENV=prod_zappa
	$(MAKE) collectstatic
	export ENV=dev_local

coderunner-build:
	cd services/code_runner/ && docker build -t $(AWS_ECR_PYTHON_REPO_NAME):latest .

coderunner-pushdocker:
	cd services/code_runner/
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com
	docker tag $(AWS_ECR_PYTHON_REPO_NAME):latest $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(AWS_ECR_PYTHON_REPO_NAME):latest
	docker push $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(AWS_ECR_PYTHON_REPO_NAME):latest

mailer-build:
	cd services/email_sender/ && docker build -t $(AWS_ECR_MAILER_REPO_NAME):latest .

mailer-pushdocker:
	cd services/email_sender/
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com
	docker tag $(AWS_ECR_MAILER_REPO_NAME):latest $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(AWS_ECR_MAILER_REPO_NAME):latest
	docker push $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(AWS_ECR_MAILER_REPO_NAME):latest

deploy: buildreact-vps-prod
	chmod +x scripts/deploy_to_server.sh
	./scripts/deploy_to_server.sh
	$(MAKE) clearstatic

export-course:
	$(ACTIVATE) && python manage.py dumpdata courses users --exclude=courses.submission --format=json --indent=4 --output=fixtures/courses.json --natural-primary --natural-foreign

zupdate-dev:
	zappa update dev

zupdate-prod:
	zappa update prod

zmanage-dev:
	zappa manage dev $(word 2,$(MAKECMDGOALS))

zmanage-prod:
	zappa manage prod $(word 2,$(MAKECMDGOALS))
