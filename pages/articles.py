from styles.article_style_sheet import *
import backend as be
import openpyxl
import os
import pandas

miniature_style: dict = dict(
    size=10,
)


class Fleche(ft.Icon):
    def __init__(self, type_mvt: str):
        super(Fleche, self).__init__(
            size=14
        )

        if type_mvt == "R":
            self.color = "lightgreen"
            self.name = ft.icons.ARROW_UPWARD
        else:
            self.color = "red"
            self.name = ft.icons.ARROW_DOWNWARD


class Miniature(ft.Container):
    def __init__(self, type_mvt: str):
        super(Miniature, self).__init__(
            border_radius=10, padding=ft.padding.only(10, 5, 10, 5)
        )

        if type_mvt == "R":
            miniature_style['color'] = "#3f6950"
            self.bgcolor = "#9fc9b0"
            self.border = ft.border.all(1, "#3f6950")
            self.content = ft.Row(
                controls=[
                    ft.Text(**miniature_style, value="Entrée")
                ], alignment='center'
            )
        else:
            miniature_style['color'] = "#c7485a"
            self.bgcolor = "#c99fa5"
            self.border = ft.border.all(1, "#c7485a")
            self.content = ft.Row(
                controls=[
                    ft.Text(**miniature_style, value="Sortie")
                ], alignment='center'
            )


class Articles(ft.Container):
    def __init__(self, ctpr: object):
        super(Articles, self).__init__(
            expand=True
        )
        self.ctpr = ctpr
        self.table = ft.DataTable(
            data_text_style=ft.TextStyle(font_family="Poppins Medium", size=11, color="black87"),
            heading_text_style=ft.TextStyle(font_family="Poppins Regular", size=11, color="grey"),
            columns=[
                ft.DataColumn(ft.Text('Référence')),
                ft.DataColumn(ft.Text('Désignation')),
                ft.DataColumn(ft.Text('Unité')),
                ft.DataColumn(ft.Text('Prix')),
                ft.DataColumn(ft.Text('Stock')),
                ft.DataColumn(ft.Text('Casier')),
                ft.DataColumn(ft.Text('')),
            ],
            rows=[]
        )
        self.filter = ft.TextField(
            **filter_style, prefix_icon='search', width=200, label="Filtrer",
            on_change=self.filter_datas
        )
        self.val_stock = ft.Text("", size=11, font_family='Poppins Regular', color="#3a5799")

        # fenêtre new article
        self.ref = ft.TextField(
            **filter_style, width=200, label="Référence",
        )
        self.des = ft.TextField(
            **filter_style, width=400, label="Désignation",
        )
        self.unite = ft.Dropdown(
            **drop_style, width=100, label="Unité",
            options=[
                ft.dropdown.Option('U'),
                ft.dropdown.Option('ML'),
                ft.dropdown.Option('F'),
            ]
        )
        self.casier = ft.TextField(
            **filter_style, width=150, label="Casier",
        )
        self.new_fen = ft.Card(
            elevation=50, surface_tint_color="white", width=400, height=430,
            left=(self.ctpr.page.window_width/2)-300, top=50,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.icons.DESCRIPTION_OUTLINED, color="#17274f", size=18),
                                ft.Text("nouvel article".upper(), size=16, font_family="Poppins Regular"),
                            ]
                        ),
                        ft.Divider(thickness=1, height=1),
                        ft.Divider(height=1, color="transparent"),
                        ft.Column([self.ref, self.des, self.unite, self.casier], spacing=20),
                        ft.Divider(height=1, color="transparent"),
                        ft.ElevatedButton(
                            bgcolor='#3a5799', height=40,
                            style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=16)),
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.icons.CHECK, size=16, color="white"),
                                    ft.Text("Valider", size=12, color="white")
                                ], alignment='center'
                            ), on_click=self.create_article
                        ),
                        ft.ElevatedButton(
                            bgcolor='#3a5799', height=40,
                            style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=16)),
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.icons.CLOSE, size=16, color="white"),
                                    ft.Text("Quitter", size=12, color="white")
                                ], alignment='center'
                            ), on_click=self.close_new_fen
                        )
                    ]
                )
            )
        )

        # fenêtre edit article
        self.e_ref = ft.TextField(
            **inactive_style, width=200, label="Référence",
        )
        self.e_des = ft.TextField(
            **filter_style, width=400, label="Désignation",
        )
        self.e_unite = ft.Dropdown(
            **drop_style, width=100, label="Unité",
            options=[
                ft.dropdown.Option('U'),
                ft.dropdown.Option('ML'),
                ft.dropdown.Option('F'),
            ]
        )
        self.e_casier = ft.TextField(
            **filter_style, label="Casier",
        )
        self.edit_fen = ft.Card(
            elevation=50, surface_tint_color="white", width=400, height=430,
            left=(self.ctpr.page.window_width/2)-300, top=50,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.icons.DESCRIPTION_OUTLINED, color="#17274f", size=18),
                                ft.Text("Modifier article".upper(), size=16, font_family="Poppins Regular"),
                            ]
                        ),
                        ft.Divider(thickness=1, height=1),
                        ft.Divider(height=1, color="transparent"),
                        ft.Column([self.e_ref, self.e_des, self.e_unite, self.e_casier], spacing=20),
                        ft.Divider(height=1, color="transparent"),
                        ft.ElevatedButton(
                            bgcolor='#3a5799', height=40,
                            style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=16)),
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.icons.CHECK, size=16, color="white"),
                                    ft.Text("Valider", size=12, color="white")
                                ], alignment='center'
                            ), on_click=self.modifier_article
                        ),
                        ft.ElevatedButton(
                            bgcolor='#3a5799', height=40,
                            style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=16)),
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.icons.CLOSE, size=16, color="white"),
                                    ft.Text("Quitter", size=12, color="white")
                                ], alignment='center'
                            ), on_click=self.close_edit_fen
                        )
                    ]
                )
            )
        )

        # fenêtre historique
        self.histo_table = ft.DataTable(
            data_text_style=ft.TextStyle(font_family="Poppins Medium", size=11, color="black87"),
            heading_text_style=ft.TextStyle(font_family="Poppins Regular", size=11, color="grey"),
            columns=[
                ft.DataColumn(ft.Text('type')),
                ft.DataColumn(ft.Text('')),
                ft.DataColumn(ft.Text('numero')),
                ft.DataColumn(ft.Text('date')),
                ft.DataColumn(ft.Text('stock avant')),
                ft.DataColumn(ft.Text('Qté bon')),
                ft.DataColumn(ft.Text('stock après')),
                ft.DataColumn(ft.Text('')),
            ],
            rows=[]
        )
        self.h_ref = ft.TextField(
            **filter_style, width=160, label="Référence"
        )
        self.h_des = ft.TextField(
            **filter_style, width=350, label="Désignation",
        )
        self.h_unite = ft.TextField(
            **filter_style, width=110, label="Unite",
        )

        self.h_qte = ft.TextField(
            **filter_style, width=90, label="Stock", input_filter=ft.NumbersOnlyInputFilter()
        )
        self.h_prix = ft.TextField(
            **filter_style, width=150, label="PMP", input_filter=ft.NumbersOnlyInputFilter()
        )
        self.h_casier = ft.TextField(
            **filter_style, width=100, label="Casier", input_filter=ft.NumbersOnlyInputFilter()
        )
        self.histo_fen = ft.Card(
            elevation=50, surface_tint_color="white", width=800, height=630,
            left=(self.ctpr.page.window_width / 2) - 600, top=0,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, shadow_color="black",
            scale=ft.transform.Scale(0), expand=True,
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                padding=20, expand=True,
                content=ft.Column(
                    expand=True,  # scroll="auto", height=150,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("Historique".upper(), size=16, font_family="Poppins Regular"),
                            ], alignment="spaceBetween"
                        ),
                        ft.Divider(height=1, thickness=1),
                        ft.Divider(height=1, color="transparent"),
                        ft.Text("Infos article".upper(), size=11),
                        ft.Container(
                            padding=10, border_radius=8, border=ft.border.all(1, "#ebebeb"),
                            content=ft.Column(
                                controls=[
                                    ft.Row([self.h_ref, self.h_des]),
                                    ft.Row([self.h_unite, self.h_qte, self.h_prix, self.h_casier]),
                                ], spacing=20
                            )
                        ),
                        ft.Divider(height=1, color="transparent"),
                        ft.Text("Table historique".upper(), size=11),
                        ft.Container(
                            expand=True, padding=ft.padding.only(10, 3, 10, 3), height=100,
                            border_radius=8, border=ft.border.all(1, "#ebebeb"),
                            content=ft.Column(
                                expand=True, scroll="auto", height=150,
                                controls=[self.histo_table],
                            )
                        ),
                        ft.ElevatedButton(
                            bgcolor='#3a5799', height=40,
                            style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=16)),
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.icons.CLOSE, size=16, color="white"),
                                    ft.Text("Quitter", size=12, color="white")
                                ], alignment='center'
                            ), on_click=self.close_histo_fen
                        )
                    ]
                )
            )
        )

        self.contenu = ft.Container(
            padding=10, expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Text("Stock".upper(), size=20, font_family="Poppins Light"),
                    ft.Divider(height=1, thickness=1),
                    ft.Container(
                        padding=10,
                        # border=ft.border.all(1, "#ebebeb"), border_radius=6,
                        content=ft.Row(
                            controls=[
                                self.filter,
                                ft.Row(
                                    controls=[
                                        # ft.Text("     Actions", size=12, color="#17274f"),
                                        ft.IconButton(
                                            ft.icons.PRINT, icon_size=22, icon_color="#17274f",
                                            tooltip="Exporter pdf"
                                        ),
                                        ft.IconButton(
                                            ft.icons.FILE_DOWNLOAD_OUTLINED, icon_size=22, icon_color="#17274f",
                                            tooltip='Import excel',
                                            on_click=lambda _: self.ctpr.fp_importer_stocks.pick_files()
                                        ),
                                        ft.IconButton(
                                            ft.icons.FILE_UPLOAD_OUTLINED, icon_size=22, icon_color="#17274f",
                                            tooltip="Exporter excel",
                                            on_click=lambda _: self.ctpr.fp_extraire_stocks.save_file(allowed_extensions=['xlsx'])
                                        ),
                                        ft.IconButton(
                                            ft.icons.POST_ADD_SHARP, icon_size=22, icon_color="#17274f",
                                            tooltip="créer Article",
                                            on_click=self.open_new_fen
                                        ),
                                    ]
                                )

                            ], alignment="spaceBetween"
                        )
                    ),
                    ft.Container(
                        expand=True, padding=ft.padding.only(5, 0, 5, 0),
                        # border_radius=8, border=ft.border.all(1, "#ebebeb"),
                        content=ft.Column(
                            expand=True, scroll='auto',
                            controls=[self.table]
                        )
                    ),


                ]
            )
        )
        self.content = ft.Stack(
            controls=[
                self.contenu,
                self.new_fen,
                self.edit_fen, self.histo_fen
            ]
        )
        self.ctpr.fp_importer_stocks.on_result = self.importer_articles
        self.ctpr.fp_extraire_stocks.on_result = self.exporter_stock

        self.load_datas()

    def load_datas(self):
        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        stock = be.all_articles_stock()
        valeur_stock = 0

        for item in stock:
            self.table.rows.append(
                ft.DataRow(
                    data=item,
                    cells=[
                        ft.DataCell(ft.Text(item['ref'])),
                        ft.DataCell(ft.Text(item['des'])),
                        ft.DataCell(ft.Text(item['unite'])),
                        ft.DataCell(ft.Text(be.milSep(item['prix']))),
                        ft.DataCell(ft.Text(item['stock'])),
                        ft.DataCell(ft.Text(item['casier'])),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        ft.icons.EDIT, icon_color="#3a5799", icon_size=15, data=item['id'],
                                        on_click=self.open_edit_fen
                                    ),
                                    ft.IconButton(
                                        ft.icons.DELETE, icon_color="red", icon_size=15, data=item['id'],
                                        on_click=self.delete_article
                                    )
                                ]
                            )
                        ),
                    ],
                    on_select_changed=self.open_historique
                )
            )
            valeur_stock += item['prix'] * item['stock']
        self.val_stock.value = f"XAF  {be.milSep(valeur_stock)}"

    def filter_datas(self, e):
        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        stock = be.all_articles_stock()
        filtre = self.filter.value.lower()

        filter_datas = list(filter(lambda x: filtre in x['ref'].lower() or filtre in x['des'].lower(), stock))

        for item in filter_datas:
            self.table.rows.append(
                ft.DataRow(
                    data=item,
                    cells=[
                        ft.DataCell(ft.Text(item['ref'])),
                        ft.DataCell(ft.Text(item['des'])),
                        ft.DataCell(ft.Text(item['unite'])),
                        ft.DataCell(ft.Text(be.milSep(item['prix']))),
                        ft.DataCell(ft.Text(item['stock'])),
                        ft.DataCell(ft.Text(item['casier'])),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        ft.icons.EDIT, icon_color="#3a5799", icon_size=15, data=item['id'],
                                        on_click=self.open_edit_fen
                                    ),
                                    ft.IconButton(
                                        ft.icons.DELETE, icon_color="red", icon_size=15, data=item['id'],
                                        on_click=self.delete_article
                                    )
                                ]
                            )
                        ),
                    ], on_select_changed=self.open_historique
                )
            )

        self.table.update()

    def open_new_fen(self, e):
        self.new_fen.scale = 1
        self.new_fen.update()

    def close_new_fen(self, e):
        for widget in (self.ref, self.des, self.unite, self.casier):
            widget.value = None
            widget.update()

        self.new_fen.scale = 0
        self.new_fen.update()

    def create_article(self, e):
        count = 0
        for widget in (self.ref, self.des, self.unite):
            if widget.value is None or widget.value == "":
                count += 1

        if count == 0:
            if be.is_exists_ref(self.ref.value):
                self.ctpr.title_box.value = "Erreur"
                self.ctpr.title_box.update()
                self.ctpr.message.value = "Cette référence existe déja"
                self.ctpr.message.update()
                self.ctpr.box.open = True
                self.ctpr.box.update()
            else:
                be.add_article(self.ref.value, self.des.value, self.unite.value, 0, self.casier.value)

                last = be.last_article_id()
                be.add_stock(last, 0)

                for widget in (self.ref, self.des, self.unite, self.casier):
                    widget.value = None
                    widget.update()

                self.ctpr.title_box.value = "Validé"
                self.ctpr.title_box.update()
                self.ctpr.message.value = "Article crée"
                self.ctpr.message.update()
                self.ctpr.box.open = True
                self.ctpr.box.update()

                self.load_datas()
                self.table.update()

        else:
            self.ctpr.title_box.value = "Erreur"
            self.ctpr.title_box.update()
            self.ctpr.message.value = "Tous les champs sont obligatoires"
            self.ctpr.message.update()
            self.ctpr.box.open = True
            self.ctpr.box.update()

    def select_ref(self, e, f, g, h ):
        self.e_ref.value = e
        self.e_des.value = f
        self.e_unite.value = g
        self.e_casier.value = h

        for widget in (self.e_ref, self.e_des, self.e_unite, self.e_casier):
            widget.update()

    def open_historique(self, e):
        self.h_ref.value = e.control.data['ref']
        self.h_des.value = e.control.data['des']
        self.h_prix.value = e.control.data['prix']
        self.h_qte.value = e.control.data['stock']
        self.h_casier.value = e.control.data['casier']
        self.h_unite.value = e.control.data['unite']

        for widget in (self.h_casier, self.h_des, self.h_prix, self.h_qte, self.h_ref, self.h_unite):
            widget.update()

        for row in self.histo_table.rows[:]:
            self.histo_table.rows.remove(row)

        all_mouvs = be.all_mouvements(e.control.data['ref'])

        for row in all_mouvs:
            self.histo_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(row['type'])),
                        ft.DataCell(Miniature(row['type'])),
                        ft.DataCell(ft.Text(row['numero'])),
                        ft.DataCell(ft.Text(row['date'])),
                        ft.DataCell(ft.Text(row['stock avt'])),
                        ft.DataCell(ft.Text(row['qte'])),
                        ft.DataCell(ft.Text(row['stock ap'])),
                        ft.DataCell(Fleche(row['type'])),
                    ]
                )
            )

        self.histo_table.update()
        self.histo_fen.scale = 1
        self.histo_fen.update()

    def close_histo_fen(self, e):
        self.histo_fen.scale = 0
        self.histo_fen.update()

    def open_edit_fen(self, e):
        infos = be.article_by_id(e.control.data)
        self.e_ref.value = infos[1]
        self.e_des.value = infos[2]
        self.e_unite.value = infos[3]
        self.e_casier.value = infos[5]

        for widget in (self.e_ref, self.e_des, self.e_unite, self.e_casier):
            widget.update()

        self.edit_fen.scale = 1
        self.edit_fen.update()

    def close_edit_fen(self, e):
        for widget in (self.e_ref, self.e_des, self.e_unite, self.e_casier):
            widget.value = None
            widget.update()

        self.edit_fen.scale = 0
        self.edit_fen.update()

    def delete_article(self, e):
        id_ref = e.control.data

        if be.is_histo_exists(id_ref):
            self.ctpr.title_box.value = "Erreur"
            self.ctpr.title_box.update()
            self.ctpr.message.value = "Suppression impossible. l'historique n'est pas vide"
            self.ctpr.message.update()
            self.ctpr.box.open = True
            self.ctpr.box.update()
        else:
            be.delete_article_by_id(id_ref)
            self.load_datas()
            self.table.update()

    def modifier_article(self, e):
        count = 0
        for widget in (self.e_ref, self.e_des, self.e_unite):
            if widget.value is None or widget.value == "":
                count += 1

        if count == 0:
            be.update_ref(self.e_des.value, self.e_unite.value, self.e_casier.value, self.e_ref.value)

            for widget in (self.e_ref, self.e_des, self.e_unite, self.e_casier):
                widget.value = None
                widget.update()

            self.ctpr.title_box.value = "Validé"
            self.ctpr.title_box.update()
            self.ctpr.message.value = "Article Modifié"
            self.ctpr.message.update()
            self.ctpr.box.open = True
            self.ctpr.box.update()

            self.load_datas()
            self.table.update()

        else:
            self.ctpr.title_box.value = "Erreur"
            self.ctpr.title_box.update()
            self.ctpr.message.value = "Tous les champs sont obligatoires"
            self.ctpr.message.update()
            self.ctpr.box.open = True
            self.ctpr.box.update()

    def importer_articles(self, e: ft.FilePickerResultEvent):
        file = e.files[0]
        absolute_path = os.path.abspath(file.path)
        workbook = openpyxl.load_workbook(absolute_path)
        sheet = workbook.active
        valeurs = list(sheet.values)
        header = valeurs[0]
        valeurs.remove(header)

        count = 0
        for row in valeurs:
            if be.is_exists_ref(row[0]):
                pass
            else:
                be.add_article(row[0], row[1], row[2], row[3], row[4])
                last = be.last_article_id()
                be.add_stock(last, 0)
                count += 1

        self.ctpr.title_box.value = "Import Réussi"
        self.ctpr.title_box.update()
        self.ctpr.message.value = f"{count} lignes imortées avec succès"
        self.ctpr.message.update()
        self.ctpr.box.open = True
        self.ctpr.box.update()

    def exporter_stock(self, e: ft.FilePickerResultEvent):
        table_datas = be.all_articles_stock()

        refs = [data['ref'] for data in table_datas]
        desigs = [data['des'] for data in table_datas]
        unites = [data['unite'] for data in table_datas]
        prices = [data['prix'] for data in table_datas]
        casiers = [data['casier'] for data in table_datas]
        stocks = [data['stock'] for data in table_datas]

        articles = {
            'référence': refs, 'désignation': desigs, 'unité': unites,
            'prix': prices, 'casier': casiers, 'stock': stocks
        }
        df = pandas.DataFrame(articles)
        save_location = f"{e.path}.xlsx"

        if save_location != "None.xlsx":
            excel = pandas.ExcelWriter(save_location)
            df.to_excel(excel, sheet_name="feuil1", index=False)
            excel.close()

            # Boîte de dialogue
            self.ctpr.title_box.value = "Validé !"
            self.ctpr.title_box.update()
            self.ctpr.message.value = "Fichier créé avec succès"
            self.ctpr.message.update()
            self.ctpr.box.open = True
            self.ctpr.box.update()
        else:
            self.ctpr.title_box.value = "Erreur"
            self.ctpr.title_box.update()
            self.ctpr.message.value = "Pas de chemin choisi"
            self.ctpr.message.update()
            self.ctpr.box.open = True
            self.ctpr.box.update()










