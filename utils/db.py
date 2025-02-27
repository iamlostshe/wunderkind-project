"""Модуль работы с базой данных."""

import json
import time
from pathlib import Path

from loguru import logger

from load_env import (
    COURSES_DB_FILE_NAME,
    PAYMENTS_DB_FILE_NAME,
    REPORTS_DB_FILE_NAME,
    STUDENTS_DB_FILE_NAME,
    TEACHERS_DB_FILE_NAME,
)


def check_db() -> None:
    """Проверяет наличие файлов баз данных, в случае отствия создаёт их."""
    for file_name in (
        COURSES_DB_FILE_NAME,
        PAYMENTS_DB_FILE_NAME,
        REPORTS_DB_FILE_NAME,
        STUDENTS_DB_FILE_NAME,
        TEACHERS_DB_FILE_NAME,
    ):
        path_file_object = Path(file_name)
        if not path_file_object.parent.exists():
            path_file_object.parent.mkdir(parents=True, exist_ok=True)
        if not path_file_object.exists():
            with path_file_object.open("a", encoding="UTF-8") as f:
                f.write("[]\n")


class Courses:
    """Работа с созданием расписания кружков в базе данных."""

    def add(
        self,
        data: dict[str: str],
    ) -> None:
        """Добавление кружка в базу данных."""
        with Path.open(COURSES_DB_FILE_NAME, "r+", encoding="UTF-8") as f:

            # Выводим лог
            logger.debug("Запись нового кружка в базу данных: {}", data)

            # Добавляем время записи в базу данных
            data["time"] = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())

            # Получаем текущую информацию в базе данных
            db_data = json.load(f)

            # Обновляем информацию (записываем информацию о кружке)
            db_data.append(data)

            # Сохраняем изменения в файл
            f.seek(0)
            f.truncate()
            json.dump(db_data, f, indent=4, ensure_ascii=False)

    def get(self) -> list:
        """Получения данных кружков."""
        with Path.open(COURSES_DB_FILE_NAME, "r", encoding="UTF-8") as f:
            return json.load(f)


class Teachers:
    """Работа с данными учителей."""

    # TODO(@iamlostshe): Добавить функционал добавления учителей
    #def add() -> None:
        #"""Добавление нового учителя."""
        #pass

    def get(self) -> list:
        """Получения данных учителей."""
        with Path.open(TEACHERS_DB_FILE_NAME, "r", encoding="UTF-8") as f:
            return json.load(f)


class Students:
    """Работа с созданием расписания кружков в базе данных."""

    def add(
        self,
        data: dict[str: str],
    ) -> None:
        """Добавление кружка в базу данных."""
        with Path.open(STUDENTS_DB_FILE_NAME, "r+", encoding="UTF-8") as f:
            # Выводим лог
            logger.debug("Запись нового ученика в базу данных: {}", data)

            # Добавляем время записи в базу данных
            data["time"] = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())

            # Получаем текущую информацию в базе данных
            db_data = json.load(f)

            # Обновляем информацию (записываем информацию о кружке)
            db_data.append(data)

            # Сохраняем изменения в файл
            f.seek(0)
            f.truncate()
            json.dump(db_data, f, indent=4, ensure_ascii=False)

    def get(self) -> list:
        """Получения данных учеников."""
        with Path.open(STUDENTS_DB_FILE_NAME, "r", encoding="UTF-8") as f:
            return json.load(f)


class Payments:
    """Класс для взимодействия с платежами."""

    def add(
        self,
        data: dict[str: str],
    ) -> None:
        """Функция для добавления новой расценки в базу данных."""
        with Path.open(PAYMENTS_DB_FILE_NAME, "r+", encoding="UTF-8") as f:
            # Записываем в бд цену за месяц и за год
            data["price_month"] = data["price"] * 7.6
            data["price_year"] = data["price"] * 59.04

            # Добавляем время записи в базу данных
            data["time"] = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())

            # Выводим лог
            logger.debug("Запись новой расценки в базу данных: {}", data)

            # Получаем текущую информацию в базе данных
            db_data = json.load(f)

            # Обновляем информацию (записываем информацию о кружке)
            db_data.append(data)

            # Сохраняем изменения в файл
            f.seek(0)
            f.truncate()
            json.dump(db_data, f, indent=4, ensure_ascii=False)

    def get(self) -> list:
        """Получения данных о платежах."""
        with Path.open(PAYMENTS_DB_FILE_NAME, "r", encoding="UTF-8") as f:
            return json.load(f)


class Reports:
    """Класс для взаимодействия с отчётми."""

    def __init__(self) -> None:
        """Инициализирует класс."""
        self.bases = {
            "База кружков": COURSES_DB_FILE_NAME,
            "База абонементов": PAYMENTS_DB_FILE_NAME,
            "База отчётов": REPORTS_DB_FILE_NAME,
            "База учеников": STUDENTS_DB_FILE_NAME,
            "База учителей": TEACHERS_DB_FILE_NAME,
        }

    def get_reports_names(self) -> list:
        """Возвращает базы, по которым доступен репорт."""
        return self.bases.keys()

    def add(
        self,
        data: dict[str: str],
    ) -> None:
        """Функция для добавления нового отчёта в базу данных."""
        with Path.open(REPORTS_DB_FILE_NAME, "r+", encoding="UTF-8") as f:
            # Добавляем время записи в базу данных
            now_time = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
            data["time"] = now_time

            # Получаем имена файлов
            file_read_name = self.bases[data["type"]]
            file_write_name = f"reports/{now_time.replace('.', '-').replace(':', '-').replace(' ', '-')}.json"  # noqa: E501

            # Записываем имя файла отчёта в базу данных
            data["file_write_name"] = file_write_name

            # Получаем текущую информацию в базе данных
            db_data = json.load(f)

            # Выводим лог
            logger.debug("Запись данных об отчёте в базу данных: {}", data)

            # Обновляем информацию (записываем информацию о кружке)
            db_data.append(data)

            # Сохраняем изменения в файл
            f.seek(0)
            f.truncate()
            json.dump(db_data, f, indent=4, ensure_ascii=False)

        # Выводим лог
        logger.debug("Создаю новый отчёт: {}", file_write_name)

        # Проверяем существует ли директория отчета

        # Создаём отчёт
        path_file_object = Path(file_write_name)

        if not path_file_object.parent.exists():
            path_file_object.parent.mkdir(parents=True, exist_ok=True)

        with Path.open(file_read_name, "r", encoding="UTF-8") as file_read:
            with path_file_object.open("a", encoding="UTF-8") as file_write:
                file_write.write(file_read.read())

    def get(self) -> list:
        """Получение данных отчётов."""
        with Path.open(REPORTS_DB_FILE_NAME, "r", encoding="UTF-8") as f:
            return json.load(f)
