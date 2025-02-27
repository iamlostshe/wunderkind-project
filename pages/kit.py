"""Модуль для работы с главной страницей."""

from __future__ import annotations

import flet as ft
from loguru import logger

from pages.nav_bar import nav_bar
from utils import db


def edit_kit_page(page: ft.Page) -> None:
    """Страница добавления новых пазлов."""
    # Инициализируем словарь для хранения информации о учащихся
    data = {
        "name": None,
        "age": None,
        "course": None,
        "parent_phone_num": None,
    }

    def student_name_on_blur(e: ft.core.control_event.ControlEvent) -> None:
        """ФИО ученика."""
        # Убирем все ошибки
        e.control.error_text = None
        page.update()

        # Получем текст из поля
        text = e.control.value

        # Выводим лог
        logger.debug("ФИО ученика: {}", text)

        # Проверяем заполнено ли поле
        if text not in ["", None]:
            if len(text.split()) == 3:  # noqa: PLR2004
                data["name"] = text
            else:
                e.control.error_text = "ФИО должно содержать 3 слова."
                page.update()

        else:
            e.control.error_text = "Это поле не должно быть пустым."
            page.update()


    def choice_of_age_on_click(e: ft.core.control_event.ControlEvent) -> None:
        """Выбор возрастного интервала."""
        # Получаем текст из поля
        text = e.control.value

        # Выводим лог
        logger.debug("Возрастной интервал: {}", text)

        # Запишем изменения в data
        data["age"] = text

    # Выбор возрастного интервала из выпадающего списка
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

    def choice_of_course_on_click(e: ft.core.control_event.ControlEvent) -> None:
        """Выбор кружка."""
        # Получаем текст из поля
        text = e.control.value

        # Выводим лог
        logger.debug("Возрастной интервал: {}", text)

        # Запишем изменения в data
        data["course"] = text

    # Получаем данные о кружках из базы данных
    c = db.Courses()
    result = [ft.dropdown.Option(i["name"]) for i in c.get()]

    if not result:
        result = [
            ft.dropdown.Option(
                "Сначала необходимо создать кружок в разделе расписание.",
            ),
        ]

    # Выбор кружка из выпадающего списка
    choice_of_course = ft.Dropdown(
        label="Выбор кружка",
        width=page.width,
        on_change=choice_of_course_on_click,
        options=result,
    )

    def check_phone_number(phone_number: str) -> tuple[bool, str]:
        """Функция для проверки корректности телефонного номера."""
        # Проверяем на недопустимые символы
        for i in "".join(phone_number.split()):
            if i not in "1234567890()+-":
                return False, 'Это поле может содержать только: "1234567890()+-".'

        # Проверяем на начало с +7
        if not phone_number.startswith("+7"):
            return False, "Номер должен начинаться с +7."

        return True, ""

    def parent_phone_num_on_blur(e: ft.core.control_event.ControlEvent) -> None:
        """Наименование кружка."""
        # Убирем все ошибки
        e.control.error_text = None
        page.update()

        # Получаем текст из поля
        text = e.control.value

        # Выводим лог
        logger.debug("Наименование кружка: {}", text)

        # Проверяем заполнено ли поле
        if text not in ["", None]:
            cpn = check_phone_number(text)
            if cpn[0]:
                data["parent_phone_num"] = text
            else:
                e.control.error_text = cpn[1]
                page.update()
        else:
            e.control.error_text = "Это поле не должно быть пустым"
            page.update()

    def back(page: ft.Page) -> None:
        """Кнопка "Назад"."""
        # Очищаем страницу
        page.clean()

        # Добавляем навигационное меню
        page.add(nav_bar(page, 1))

        # Открываем страницу расписания
        page.add(kit_page(page))

    def submit_form(e: ft.core.control_event.ControlEvent, page: ft.Page) -> None:  # noqa: ARG001
        """Сохраняет результат формы."""
        # Получаем непустые строки
        len_data = 0

        for i in data.values():
            if i not in ["", None]:
                len_data += 1

        # Если информации достаточно
        if len_data == 4:
            # Записываем её в JSON бд
            s = db.Students()
            s.add(data)

            # Очищаем страницу
            page.clean()

            # Переходим на главную
            page.add(kit_page(page))

            # Добавляем навигационное меню
            page.add(nav_bar(page, 1))

        else:
            # В ином случае выводим предупреждение
            page.snack_bar = ft.SnackBar(ft.Text("Нужно заполнить все поля"), open=True)
            page.update()

            logger.error("Заполнены не все поля.")

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
                    label="ФИО ученика",
                    on_blur=student_name_on_blur,
                ),
                choice_of_age,
                choice_of_course,
                ft.TextField(
                    label="№ телефона родителя",
                    on_blur=parent_phone_num_on_blur,
                ),
                ft.Row(controls=[submit], alignment=ft.MainAxisAlignment.CENTER),
            ],
        ),
    )


def kit_page(page: ft.Page) -> ft.SafeArea:
    """Главное меню."""
    def plus_button_on_click(
        e: ft.core.control_event.ControlEvent,  # noqa: ARG001
        page: ft.Page,
    ) -> None:
        """Нажатие на кнопку "+"."""
        # Очищаем страницу
        page.clean()

        # Добавляем навигационное меню
        page.add(nav_bar(page, 1))

        # Добавляем страницу создания пазлов
        page.add(edit_kit_page(page))

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
                    ft.Text("Пока не записано ни одного ученика."),
                ],
            )
        # Инициализируем пустой список для названий колнок
        columns = []

        # Подписываем колонки
        for column_name in (
            "№",
            "ФИО",
            "Возраст",
            "Кружок",
            "№ телефона родителя",
            "Время создания заявки",
        ):
            columns.append(ft.DataColumn(ft.Text(column_name)))

        # Инициализируем пустой список для строк
        rows = []

        # Записываем строки
        for c, row in enumerate(items):
            # Инициализируем пустой список под клетки
            cells = [ft.DataCell(ft.Text(c + 1))]

            # Проходимся по всем клеткам строки
            cells += [ft.DataCell(ft.Text(row[i])) for i in row]

            # Добавляем строку
            rows.append(ft.DataRow(cells))

        # Возвращаем таблицу
        return ft.DataTable(width=page.width, columns=columns, rows=rows)

    # Получаем информацию из бд
    s = db.Students()
    table = get_table(s.get())

    # Возвращаем страницу
    return ft.SafeArea(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.TextField(
                            label="TODO: Поиск по ученикам.",
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
