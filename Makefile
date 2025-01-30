start:
	poetry run flask --app app run --port 8000

start_debug:
	poetry run flask --app app --debug run --port 8000

build:
	./build.sh