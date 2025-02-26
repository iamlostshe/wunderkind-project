"""Модуль для работы с главной страницей."""

from __future__ import annotations

import flet as ft

# from pages.nav_bar import nav_bar  # noqa: ERA001
# from utils import db  # noqa: ERA001


def edit_kit_page(page: ft.Page) -> None:
    """Страница добавления новых пазлов."""
    # Возвращаем страницу
    return ft.SafeArea(
        ft.Column(
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            width=page.width,
            controls=[
                ft.Text(value="Редактирование наборов."),
            ],
        ),
    )


def kit_page(page: ft.Page) -> ft.SafeArea:
    """Главное меню."""
    # Возвращаем страницу
    return ft.SafeArea(
        ft.Column(
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            width=page.width,
            controls=[
                ft.Text(value="Страница наборов."),
            ],
        ),
    )
