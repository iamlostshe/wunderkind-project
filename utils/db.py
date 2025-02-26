"""Модуль работы с базой данных."""

import json
from pathlib import Path
from time import time

from load_env import COURSES_DB_FILE_NAME


def check_db() -> None:
    """Проверяет наличие файлов баз данных, в случае отствия создаёт их."""
    for file_name in (
        COURSES_DB_FILE_NAME,
    ):
        path_file_object = Path(file_name)
        if not path_file_object.parent.exists():
            path_file_object.parent.mkdir(parents=True, exist_ok=True)
        if not path_file_object.exists():
            with path_file_object.open("a", encoding="UTF-8") as f:
                f.write("[]\n")


class Schedule:
    """Работа с созданием расписания кружков в базе данных."""

    def __init__(self) -> None:
        """Инициализация класса."""
        self.now_time = time()

    def add(
        self,
        data: dict[str: str],
    ):
        """Добавление кружка в базу данных."""
        with Path.open(COURSES_DB_FILE_NAME, "r+", encoding="UTF-8") as f:
            # Получаем текущую информацию в базе данных
            db_data = json.load(f)

            # Обновляем информацию (записываем информацию о кружке)
            db_data.append(data)

            # Сохраняем изменения в файл
            f.seek(0)
            f.truncate()
            json.dump(db_data)
