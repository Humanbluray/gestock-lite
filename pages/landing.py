import flet as ft
import backend as be


class Landing(ft.View):
    def __init__(self, page):
        super(Landing, self).__init__(
            horizontal_alignment="center", route="/",  vertical_alignment='center',
        )
        self.page = page

        self.login = ft.TextField(
            label="login", height=45, dense=True,
            prefix_icon="person", border_color="#f0f0f6", bgcolor="#f0f0f6",
            border_radius=10, cursor_height=24, content_padding=12,
            label_style=ft.TextStyle(font_family="Poppins Medium", size=12),
            text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
            # focused_border_color="#FFC39B"
        )
        self.passw = ft.TextField(
            label="password", height=45, dense=True,
            prefix_icon="key", border_color="#f0f0f6", bgcolor="#f0f0f6",
            border_radius=10, cursor_height=24, content_padding=12,
            label_style=ft.TextStyle(font_family="Poppins Medium", size=12),
            text_style=ft.TextStyle(font_family="Poppins Medium", size=12),
            password=True, can_reveal_password=True,
            # focused_border_color="#FFC39B"
        )
        self.box = ft.AlertDialog(
            surface_tint_color="white",
            title=ft.Text("Erreur", size=20, font_family="Poppins Light"),
            content=ft.Text("Login ou mot de passe incorrect", size=12),
            actions=[ft.TextButton("Quitter", on_click=self.close_box)]
        )
        self.page.overlay.append(self.box)
        self.controls = [
            ft.Container(
                padding=20, width=250, border_radius=8, border=ft.border.all(1, "#e6e6e6"),
                content=ft.Column(
                    controls=[
                        ft.Text("Login", font_family="Poppins ExtraBold", size=24),
                        ft.Divider(height=3, color="transparent"),
                        self.login, self.passw,
                        ft.Divider(height=3, color="transparent"),
                        ft.ElevatedButton(
                            style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=20)),
                            height=45,
                            content=ft.Row(
                               controls=[
                                   ft.Icon(name="CENTER_FOCUS_WEAK_ROUNDED", size=16, color="white"),
                                   ft.Text("Connecter", size=12, font_family="Poppins Medium", color="white")
                               ], alignment="center"
                            ), bgcolor="#3a5799",
                            on_click=self.connecter
                        )
                    ], horizontal_alignment="center", spacing=15,
                )
            )
        ]

    def connecter(self, e):
        if be.check_login(self.login.value, self.passw.value):
            self.page.go('/accueil')
        else:
            self.box.open = True
            self.box.update()

    def close_box(self, e):
        self.box.open = False
        self.box.update()

