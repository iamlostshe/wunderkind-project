"""Загружаем константы из .env."""

from os import getenv

from dotenv import load_dotenv

# Загружаем данные из .env
load_dotenv()

# Получаем название базы данных курсов
COURSES_DB_FILE_NAME = getenv("COURSES_DB_FILE_NAME")

# Получаем название базы данных учителей
TEACHERS_DB_FILE_NAME = getenv("TEACHERS_DB_FILE_NAME")

# Получаем название базы данных учеников (пользователей)
STUDENTS_DB_FILE_NAME = getenv("STUDENTS_DB_FILE_NAME")
