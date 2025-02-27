"""Модуль для работы с главной страницей."""

from __future__ import annotations

import flet as ft

# from pages.nav_bar import nav_bar  # noqa: ERA001
# from utils import db  # noqa: ERA001


def edit_payment_page(page: ft.Page) -> None:
    """Страница добавления новых пазлов."""
    # Возвращаем страницу
    return ft.SafeArea(
        ft.Column(
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            width=page.width,
            controls=[
                ft.Text(value="Редактирование платежей."),
            ],
        ),
    )


def payment_page(page: ft.Page) -> ft.SafeArea:
    """Главное меню."""
    # Кнопка добавления нового платежа
    plus_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        on_click=lambda e: plus_button_on_click(e, page),
    )

    # Возвращаем страницу
    return ft.SafeArea(
        ft.Column(
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            width=page.width,
            controls=[
                ft.Row(
                    controls=[
                        ft.TextField(
                            label="TODO: Поиск по платежам.",
                            expand=True,
                            # TODO(@iamlostshe): on_blur=lambda e: search_puzzles(e, page),
                        ),
                        plus_button,
                    ],
                ),
                ft.Text(value="У вас пока нет ни одного платежа."),
            ],
        ),
    )
