"""Модуль для работы с главной страницей."""

from __future__ import annotations

import flet as ft
from loguru import logger

from pages.nav_bar import nav_bar
from utils import db


def edit_report_page(page: ft.Page) -> None:
    """Страница добавления новых пазлов."""
    # Инициализируем словарь для хранения информации о отчётах
    data = {
        "type": None,
    }

    def choice_of_report_on_click(e: ft.core.control_event.ControlEvent) -> None:
        """Выбор вида отчёта."""
        # Получаем текст из поля
        text = e.control.value

        # Выводим лог
        logger.debug("Вид отчёта: {}", text)

        # Запишем изменения в data
        data["type"] = text

    # Выбор отчёта из выпадающего списка
    choice_of_report = ft.Dropdown(
        label="Выбор отчёта",
        width=page.width,
        on_change=choice_of_report_on_click,
        options=[ft.dropdown.Option(i) for i in db.Reports().get_reports_names()],
    )

    def back(page: ft.Page) -> None:
        """Кнопка "Назад"."""
        # Очищаем страницу
        page.clean()

        # Добавляем навигационное меню
        page.add(nav_bar(page, 3))

        # Открываем страницу расписания
        page.add(report_page(page))

    def submit_form(e: ft.core.control_event.ControlEvent, page: ft.Page) -> None:  # noqa: ARG001
        """Сохраняет результат формы."""
        # Получаем непустые строки
        len_data = 0

        for i in data.values():
            if i not in ["", None]:
                len_data += 1

        # Если информации достаточно
        if len_data == 1:
            # Записываем её в JSON бд
            db.Reports().add(data)

            # Очищаем страницу
            page.clean()

            # Переходим на главную
            page.add(report_page(page))

            # Добавляем навигационное меню
            page.add(nav_bar(page, 3))

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
                choice_of_report,
                ft.Row(controls=[submit], alignment=ft.MainAxisAlignment.CENTER),
            ],
        ),
    )


def report_page(page: ft.Page) -> ft.SafeArea:
    """Главное меню."""
    def plus_button_on_click(
        e: ft.core.control_event.ControlEvent,  # noqa: ARG001
        page: ft.Page,
    ) -> None:
        """Нажатие на кнопку "+"."""
        # Очищаем страницу
        page.clean()

        # Добавляем навигационное меню
        page.add(nav_bar(page, 3))

        # Добавляем страницу создания пазлов
        page.add(edit_report_page(page))

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
                    ft.Text("Вы пока не создали ни одного отчёта."),
                ],
            )

        # Подписываем колонки
        columns = [
            ft.DataColumn(ft.Text(column_name)) for column_name in (
                "№",
                "Тип",
                "Время",
                "Название файла",
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
    table = get_table(db.Reports().get())

    # Возвращаем страницу
    return ft.SafeArea(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.TextField(
                            label="TODO: Поиск по отчётам",
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
