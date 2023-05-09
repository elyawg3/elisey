install:
	pip install poetry && \
	pip install telebot
	poetry install

start:
	poetry run python "C:\Users\elise\PycharmProjects\pythonProject\main.py"