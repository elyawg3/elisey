install:
	pip install poetry && \
	telebot install
	poetry install

start:
	poetry run python "C:\Users\elise\PycharmProjects\pythonProject\main.py"