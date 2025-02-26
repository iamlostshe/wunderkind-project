"""Загружаем константы из .env."""

from os import getenv

from dotenv import load_dotenv

# Загружаем данные из .env
load_dotenv()

# Получаем данные базы данных
COURSES_DB_FILE_NAME = getenv("COURSES_DB_FILE_NAME")

# Получаем данные базы данных учителей
TEACHERS_DB_FILE_NAME = getenv("TEACHERS_DB_FILE_NAME")
