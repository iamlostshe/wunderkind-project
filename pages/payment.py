"""Модуль для работы с главной страницей."""

from __future__ import annotations

import flet as ft
from loguru import logger

from pages.nav_bar import nav_bar
from utils import db


def edit_payment_page(page: ft.Page) -> None:
    """Страница добавления новых пазлов."""
    # Инициализируем словарь для хранения информации о учащихся
    data = {}

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

    def price_on_blur(e: ft.core.control_event.ControlEvent) -> None:
        """Цена кружка."""
        # Убирем все ошибки
        e.control.error_text = None
        page.update()

        # Получаем текст из поля
        text = e.control.value

        # Выводим лог
        logger.debug("Цена кружка: {}", text)

        # Проверяем заполнено ли поле
        if text not in ["", None]:
            if text.isnumeric():
                data["price"] = float(text)
            else:
                e.control.error_text = "Ввод должен быть числом"
                page.update()
        else:
            e.control.error_text = "Это поле не должно быть пустым"
            page.update()

    def back(page: ft.Page) -> None:
        """Кнопка "Назад"."""
        # Очищаем страницу
        page.clean()

        # Добавляем навигационное меню
        page.add(nav_bar(page, 2))

        # Открываем страницу расписания
        page.add(payment_page(page))

    def submit_form(e: ft.core.control_event.ControlEvent, page: ft.Page) -> None:  # noqa: ARG001
        """Сохраняет результат формы."""
        # Если информации достаточно
        if len(data) == 2:  # noqa: PLR2004
            # Записываем её в JSON бд
            p = db.Payments()
            p.add(data)

            # Очищаем страницу
            page.clean()

            # Переходим на главную
            page.add(payment_page(page))

            # Добавляем навигационное меню
            page.add(nav_bar(page, 2))

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
                choice_of_course,
                ft.TextField(
                    label="Цена занятия",
                    on_blur=price_on_blur,
                ),
                ft.Row(controls=[submit], alignment=ft.MainAxisAlignment.CENTER),
            ],
        ),
    )


def payment_page(page: ft.Page) -> ft.SafeArea:
    """Главное меню."""
    def plus_button_on_click(
        e: ft.core.control_event.ControlEvent,  # noqa: ARG001
        page: ft.Page,
    ) -> None:
        """Нажатие на кнопку "+"."""
        # Очищаем страницу
        page.clean()

        # Добавляем навигационное меню
        page.add(nav_bar(page, 2))

        # Добавляем страницу создания пазлов
        page.add(edit_payment_page(page))

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
                    ft.Text("Пока не записано ни одного платежа."),
                ],
            )

        # Подписываем колонки
        columns = [
            ft.DataColumn(ft.Text(column_name)) for column_name in (
                "№",
                "Кружок",
                "Разовое занятие",
                "Абонемент на месяц",
                "Абонемент на год",
                "Время",
            )
        ]

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
    p = db.Payments()
    table = get_table(p.get())

    # Возвращаем страницу
    return ft.SafeArea(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.TextField(
                            label="TODO: Поиск по платежам",
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
