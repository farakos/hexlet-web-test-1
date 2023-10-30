start:
	 poetry run flask --app ./hexlet_web_test_1/example.py --debug run --port 8000

run:
	poetry run gunicorn --workers=4 --bind=127.0.0.1:8000 hexlet_web_test_1.example:app
