import flet as ft

filter_style: dict = dict(
    dense=True, height=40,
    border_color="#f0f0f6", bgcolor="#f0f0f6",
    content_padding=12, cursor_height=20,
    label_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    border_radius=6,
    capitalization=ft.TextCapitalization.CHARACTERS,
)
inactive_style: dict = dict(
    dense=True, height=40,
    disabled=True,
    content_padding=12, cursor_height=20,
    label_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    hint_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins Medium"),
    border_radius=6,
    capitalization=ft.TextCapitalization.CHARACTERS,
)
drop_style: dict = dict(
    dense=True, height=40, border_radius=6, bgcolor="#f0f0f6", border_color="#f0f0f6",
    content_padding=12, label_style=ft.TextStyle(size=12, color="#17274f", font_family="Poppins Medium"),
    text_style=ft.TextStyle(size=12, font_family="Poppins Medium", color="#17274f")
)
