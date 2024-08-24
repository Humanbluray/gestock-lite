from components import *


class Accueil(ft.View):
    def __init__(self, page):
        super(Accueil, self).__init__(
             horizontal_alignment="center", route="/accueil",
        )
        self.page = page
        self.menu = Menu(self)
        self.barre = ft.Container(
            content=self.menu,
            width=160,
        )
        self.contenu = ft.Container(
            padding=10,
            border_radius=0, border=ft.border.only(left=ft.BorderSide(1, "#e6e6e6")),
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("", size=16, font_family="Poppins Regular"),
                        ]
                    )
                ],
            )
        )
        # Dialog box
        self.title_box = ft.Text("", size=20, font_family="Poppins Light")
        self.message = ft.Text("", size=12)
        self.box = ft.AlertDialog(
            surface_tint_color="white",
            title=self.title_box,
            content=self.message,
            actions=[ft.TextButton("Quitter", on_click=self.close_box)]
        )

        # Overlays _________________________________________________________

        # stock
        self.fp_importer_stocks = ft.FilePicker()
        self.fp_extraire_stocks = ft.FilePicker()

        # entrées
        self.dp_new_entree = ft.DatePicker()
        self.fp_extraire_entrees = ft.FilePicker()
        self.fp_extraire_entrees_vue = ft.FilePicker()

        # sorties
        self.dp_new_sortie = ft.DatePicker()
        self.fp_extraire_sorties = ft.FilePicker()
        self.fp_extraire_sorties_vue = ft.FilePicker()

        for widget in (self.box, self.fp_extraire_stocks, self.fp_importer_stocks, self.dp_new_entree,
                       self.fp_extraire_entrees, self.fp_extraire_entrees_vue,
                       self.fp_extraire_sorties, self.fp_extraire_sorties_vue,
                       self.dp_new_sortie):
            self.page.overlay.append(widget)

        self.controls = [
            ft.Container(
                expand=True,
                content=ft.Row(
                    expand=True,
                    controls=[
                        self.barre,
                        self.contenu
                    ],
                )
            )
        ]

    def close_box(self, e):
        self.box.open = False
        self.box.update()










