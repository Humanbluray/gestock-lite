import flet as ft
from pages.articles import Articles
from pages.entrees import Entrees
from pages.sorties import Sorties


class ItemMenu(ft.Container):
    def __init__(self, title: str, icone: str):
        super(ItemMenu, self).__init__(
            bgcolor="white",
            border_radius=16,
            on_hover=self.hover_ct,
            shape=ft.ContinuousRectangleBorder(radius=16),
            padding=12,
            width=135,
        )
        self.title = title
        self.icone = icone
        self.is_clicked = False

        self.content = ft.Row(
            controls=[
                ft.Icon(icone, size=18, color=ft.colors.BLACK87),
                ft.Text(title, size=12, font_family="Poppins Medium", color=ft.colors.BLACK87)
            ], alignment='center'
        )

    def hover_ct(self, e):
        if e.data == "true":
            e.control.bgcolor = "#e6edff"
            e.control.content.controls[0].color = "#3a5799"
            e.control.content.controls[1].color = "#3a5799"
            e.control.content.controls[0].update()
            e.control.content.controls[1].update()
            e.control.update()
        else:
            if self.is_clicked:
                e.control.bgcolor = "#3a5799"
                e.control.content.controls[0].color = "white"
                e.control.content.controls[1].color = "white"
                e.control.content.controls[0].update()
                e.control.content.controls[1].update()
                e.control.update()
            else:
                e.control.bgcolor = "white"
                e.control.content.controls[0].color = ft.colors.BLACK87
                e.control.content.controls[1].color = ft.colors.BLACK87
                e.control.content.controls[0].update()
                e.control.content.controls[1].update()
                e.control.update()

    def set_is_clicked_true(self):
        self.is_clicked = True
        self.bgcolor = "#3a5799"
        self.content.controls[0].color = "white"
        self.content.controls[1].color = "white"
        self.content.controls[0].update()
        self.content.controls[1].update()
        self.update()

    def set_is_clicked_false(self):
        self.is_clicked = False
        self.bgcolor = "white"
        self.content.controls[0].color = ft.colors.BLACK87
        self.content.controls[1].color = ft.colors.BLACK87
        self.content.controls[0].update()
        self.content.controls[1].update()
        self.update()


class Menu(ft.Container):
    def __init__(self, container_parent: object):
        super(Menu, self).__init__(
            padding=ft.padding.only(2, 15, 6, 15),
            bgcolor="white",
            # border=ft.border.only(right=ft.BorderSide(1, "black54"))
        )
        self.container_parent = container_parent
        self.articles = ItemMenu("Stock", ft.icons.WINDOW)
        self.entrees = ItemMenu("Entrées", ft.icons.INVENTORY_SHARP)
        self.sorties = ItemMenu("Sorties", ft.icons.FULLSCREEN_EXIT)
        self.exit = ItemMenu("Quitter", ft.icons.EXIT_TO_APP_OUTLINED)
        self.childrens = [self.articles, self.entrees, self.sorties, self.exit]

        for item in self.childrens:
            item.on_click = self.cliquer_menu

        self.content = ft.Column(
            expand=True,
            controls=[
                ft.Text("M E N U", size=16, font_family="Poppins Regular"),
                ft.Divider(thickness=1, color="transparent"),
                ft.Column(
                    controls=[
                        self.articles,
                        self.entrees,
                        self.sorties,
                    ], spacing=15
                ),

                # ft.Divider(thickness=1, color="transparent"),
                ft.Divider(thickness=1, height=1),
                self.exit
            ], horizontal_alignment="center",
        )

    def cliquer_menu(self, e):
        for item in self.childrens:
            item.set_is_clicked_false()

        e.control.set_is_clicked_true()
        e.control.update()

        for row in self.container_parent.contenu.content.controls[:]:
            self.container_parent.contenu.content.controls.remove(row)

        if e.control.content.controls[1].value == "Stock":
            self.container_parent.contenu.content.controls.append(Articles(self.container_parent))
            self.container_parent.update()

        elif e.control.content.controls[1].value == "Entrées":
            self.container_parent.contenu.content.controls.append(Entrees(self.container_parent))
            self.container_parent.update()

        elif e.control.content.controls[1].value == "Sorties":
            self.container_parent.contenu.content.controls.append(Sorties(self.container_parent))
            self.container_parent.update()

        elif e.control.content.controls[1].value == "Quitter":
            self.container_parent.page.go('/')
            self.container_parent.update()





