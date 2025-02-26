"""Модуль для работы с навигационным меню."""

from __future__ import annotations

import flet as ft

SCHEDULE_PAGE_INDEX = 0 # Расписание
KIT_PAGE_INDEX = 1 # Набор
PAYMENT_PAGE_INDEX = 2 # Оплата


def nav_bar(page: ft.Page, index: int | None = 0) -> ft.NavigationBar:
    """Создаёт навигационное меню."""
    return ft.NavigationBar(
        on_change=lambda e: nav_bar_on_change(e, page),
        selected_index=index,
        destinations=[
            ft.NavigationBarDestination(
                label="Расписание",
                icon=ft.Icons.HOME_ROUNDED,
                selected_icon=ft.Icons.HOME_OUTLINED,
            ),
            ft.NavigationBarDestination(
                label="Набор",
                icon=ft.Icons.PEOPLE,
                selected_icon=ft.Icons.PEOPLE_OUTLINED,
            ),
            ft.NavigationBarDestination(
                label="Оплата",
                icon=ft.Icons.DOCUMENT_SCANNER_ROUNDED,
                selected_icon=ft.Icons.DOCUMENT_SCANNER_OUTLINED,
            ),
        ],
    )


def nav_bar_on_change(e: ft.core.control_event.ControlEvent, page: ft.Page) -> None:
    """Запускается при изменении навигационного меню."""
    from pages.kit import kit_page
    from pages.payment import payment_page
    from pages.schedule import schedule_page

    # Определяем какая страница выбрана
    num = int(e.data)

    # Очищаем страницу
    page.clean()

    # Добавляем навигационное меню
    page.add(nav_bar(page, num))

    # Расписание
    if num == SCHEDULE_PAGE_INDEX:
        page.add(schedule_page(page))

    # Набор
    elif num == KIT_PAGE_INDEX:
        page.add(kit_page(page))

    # Оплата
    elif num == PAYMENT_PAGE_INDEX:
        page.add(payment_page(page))
