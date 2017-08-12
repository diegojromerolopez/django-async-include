all: tests

tests:
	virtualenv venv
	./venv/bin/pip install -r requirements.txt
	./venv/bin/python async_include/tests/manage.py migrate
	./venv/bin/python -m pytest async_include/tests
