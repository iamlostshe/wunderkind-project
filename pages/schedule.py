"""Модуль для работы с главной страницей."""

from __future__ import annotations

import flet as ft
from loguru import logger

from pages.nav_bar import nav_bar
from utils import db


def edit_schedule_page(page: ft.Page) -> None:
    """Страница добавления новых пазлов."""
    # Инициализируем словарь для хранения информации о учащихся
    data = {
        "age": None,
        "name": None,
        "description": None,
        "teacher": None,
    }

    # Функция выбора возраста
    def choice_of_age_on_click(e: ft.core.control_event.ControlEvent) -> None:
        """Выбор возрастного интервала."""
        # Получаем текст из поля
        text = e.control.value

        # Выводим лог
        logger.debug("Возрастной интервал: {}", text)

        # Запишем изменения в data
        data["age"] = text


    def course_teacher_on_blur(e: ft.core.control_event.ControlEvent) -> None:
        """Описание кружка."""
        # Убирем все ошибки
        e.control.error_text = None

        # Получем текст из поля
        text = e.control.value

        # Выводим лог
        logger.debug("Описание кружка: {}", text)

        # Проверяем заполнено ли поле
        if text:
            if len(text.split()) == 3:  # noqa: PLR2004
                data["teacher"] = text
            else:
                e.control.error_text = "ФИО преподавателя должно содержать 3 слова."

        else:
            e.control.error_text = "Это поле не должно быть пустым."

    result = []
    t = db.Teachers()
    for teacher in t.get():
        result.append(ft.dropdown.Option(teacher))  # noqa: PERF401

    # Создаём обект для хранения учителей
    choice_of_age = ft.Dropdown(
        label="Выбор возрастного интервала",
        width=page.width,
        on_change=choice_of_age_on_click,
        options=result,
    )

    # Создаём обект для хранения возрастных интервалов
    choice_of_age = ft.Dropdown(
        label="Выбор возрастного интервала",
        width=page.width,
        on_change=choice_of_age_on_click,
        options=[
            ft.dropdown.Option("Младший дошкольный возраст (3-5 лет)"),
            ft.dropdown.Option("Старший дошкольный возраст (5-7 лет)"),
            ft.dropdown.Option("Младший школьный возраст (7-10 лет)"),
            ft.dropdown.Option("Средний школьный возраст (10-14 лет)"),
            ft.dropdown.Option("Старший школьный возраст (14-17 лет)"),
        ],
    )

    def back(page: ft.Page) -> None:
        """Кнопка "Назад"."""
        # Очищаем страницу
        page.clean()

        # Добавляем навигационное меню
        page.add(nav_bar(page, 0))

        # Открываем страницу расписания
        page.add(schedule_page(page))

    def course_name_on_blur(e: ft.core.control_event.ControlEvent) -> None:
        """Наименование кружка."""
        # Убирем все ошибки
        e.control.error_text = None

        # Получаем текст из поля
        text = e.control.value

        # Выводим лог
        logger.debug("Наименование кружка: {}", text)

        # Проверяем заполнено ли поле
        if text:
            data["name"] = text
        else:
            e.control.error_text = "Это поле не должно быть пустым"

    def course_description_on_blur(e: ft.core.control_event.ControlEvent) -> None:
        """Описание кружка."""
        # Убирем все ошибки
        e.control.error_text = None

        # Получем текст из поля
        text = e.control.value

        # Выводим лог
        logger.debug("Описание кружка: {}", text)

        # Проверяем заполнено ли поле
        if text:
            data["description"] = text
        else:
            e.control.error_text = "Это поле не должно быть пустым"

    def submit_form(e: ft.core.control_event.ControlEvent, page: ft.Page) -> None:  # noqa: ARG001
        """Сохраняет результат формы."""
        # Получаем непустые строки
        len_data = 0

        for i in data.items():
            if i:
                len_data += 1

        # Если информации достаточно
        if len_data >= 4:
            # Записываем её в JSON бд
            s = db.Courses()
            s.add(data)

            # Очищаем страницу
            page.clean()

            # Переходим на главную
            page.add(schedule_page(page))

            # Добавляем навигационное меню
            page.add(nav_bar(page, 0))

        else:
            # В ином случае выводим предупреждение
            page.snack_bar = ft.SnackBar(ft.Text("Нужно заполнить все поля"))
            page.snack_bar.open = True
            page.update()

    # Кнопка подтверждения отправки данных
    submit = ft.CupertinoFilledButton(
        "Продолжить",
        width=page.width,
        on_click=lambda e: submit_form(e, page),
    )

    # Возвращаем страницу
    return ft.SafeArea(
        ft.Column(
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            width=page.width,
            controls=[
                ft.CupertinoFilledButton(
                    "Назад",
                    width=page.width,
                    icon=ft.Icons.ARROW_BACK_IOS_NEW,
                    on_click=lambda e: back(page),  # noqa: ARG005
                ),
                ft.TextField(
                    label="Наименование кружка",
                    on_blur=course_name_on_blur,
                ),
                choice_of_age,
                ft.TextField(
                    label="Описание кружка",
                    on_blur=course_description_on_blur,
                ),
                ft.TextField(
                    label="Преподаватель",
                    on_blur=course_teacher_on_blur,
                ),
                ft.Row(controls=[submit], alignment=ft.MainAxisAlignment.CENTER),
            ],
        ),
    )


def schedule_page(page: ft.Page) -> ft.SafeArea:
    """Главное меню."""
    def plus_button_on_click(
        e: ft.core.control_event.ControlEvent,  # noqa: ARG001
        page: ft.Page,
    ) -> None:
        """Нажатие на кнопку "+"."""
        # Очищаем страницу
        page.clean()

        # Добавляем навигационное меню
        page.add(nav_bar(page, 0))

        # Добавляем страницу создания пазлов
        page.add(edit_schedule_page(page))

    # Кнопка добавления нового кружка
    plus_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        on_click=lambda e: plus_button_on_click(e, page),
    )

    def get_table(items: list) -> ft.Row | ft.DataTable:
        """Функция для создания таблицы."""
        # Если в бд нет ни одного товара
        if not items:
            return ft.Row(
                controls=[
                    ft.Text("У Вас пока нет ни одного шаблона пазла("),
                ],
            )
        # Инициализируем пустой список для названий колнок
        columns = []

        # Подписываем колонки
        for column_name in (
            "№",
            "Возраст",
            "Название",
            "Описание",
            "Преподаватель",
            "Время",
        ):
            columns.append(ft.DataColumn(ft.Text(column_name)))

        # Инициализируем пустой список для строк
        rows = []

        # Записываем строки
        for c, row in enumerate(items):
            # Инициализируем пустой список под клетки
            cells = [ft.DataCell(ft.Text(c + 1))]

            # Проходимся по всем клеткам строки
            for i in row:
                # Добавляем новую клетку
                cells.append(ft.DataCell(ft.Text(row[i])))

            # Добавляем строку
            rows.append(ft.DataRow(cells))

        # Возвращаем таблицу
        return ft.DataTable(width=page.width, columns=columns, rows=rows)

    # Получаем информацию из бд
    c = db.Courses()
    table = get_table(c.get())

    # Возвращаем страницу
    return ft.SafeArea(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.TextField(
                            label="TODO: Поиск по расписанию.",
                            expand=True,
                            # TODO(@iamlostshe): on_blur=lambda e: search_puzzles(e, page),
                        ),
                        plus_button,
                    ],
                ),
                table,
            ],
        ),
    )
