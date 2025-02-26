"""Запуск приложения."""

import flet as ft
from loguru import logger

from pages.nav_bar import nav_bar
from pages.schedule import schedule_page
from utils import db


def main(page: ft.Page) -> None:
    """Функция для запуска приложения."""
    # Проверяем наличае JSON базы данных
    db.check_db()

    # Подключаем файл для логов
    logger.add("wunderkind-project.log")

    # Задаём название приложению
    page.title = "wunderkind-project"

    # Добавляем навигационное меню
    page.add(nav_bar(page))

    # Открываем стартовую страницу
    page.add(schedule_page(page))


if __name__ == "__main__":
    ft.app(target=main)
