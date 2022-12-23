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