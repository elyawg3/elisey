install:
	pip install poetry && \
	pip install pyTelegramBotAPI
	poetry install

start:
	poetry run python "C:\Users\elise\PycharmProjects\pythonProject\main.py"