from styles.article_style_sheet import *
import backend as be
import pandas


class Sorties(ft.Container):
    def __init__(self, ctpr: object):
        super(Sorties, self).__init__(
            expand=True
        )
        self.ctpr = ctpr
        self.table = ft.DataTable(
            data_text_style=ft.TextStyle(font_family="Poppins Medium", size=11, color="black87"),
            heading_text_style=ft.TextStyle(font_family="Poppins Regular", size=11, color="grey"),
            columns=[
                ft.DataColumn(ft.Text('Numero')),
                ft.DataColumn(ft.Text('Date')),
                ft.DataColumn(ft.Text('reference')),
                ft.DataColumn(ft.Text('Désignation')),
                ft.DataColumn(ft.Text('Qté')),
                ft.DataColumn(ft.Text('Imputation')),
            ],
            rows=[]
        )
        self.filter = ft.TextField(
            **filter_style, prefix_icon='search', width=200, label="Filtrer",
            on_change=self.filter_datas
        )

        # fenêtre new entree
        self.sel_date = ft.TextField(**inactive_style, label="Date", width=120)
        self.bt_select_date = ft.IconButton(
            ft.icons.EDIT_CALENDAR_ROUNDED,
            icon_size=18, bgcolor="#f0f0f6", icon_color="#092548",
            on_click=lambda _: self.ctpr.dp_new_sortie.pick_date(),
        )
        self.search_ref = ft.TextField(
            **filter_style, width=300, label="Référence", prefix_icon="search",
            on_change=self.filter_ref
        )
        self.new_ref_table = ft.DataTable(
            data_text_style=ft.TextStyle(font_family="Poppins Medium", size=11, color="black87"),
            heading_text_style=ft.TextStyle(font_family="Poppins Regular", size=11, color="grey"),
            columns=[
                ft.DataColumn(ft.Text('reference')),
                ft.DataColumn(ft.Text('Désignation')),
            ],
            rows=[]
        )
        self.ref = ft.TextField(**inactive_style, width=160, label="Référence")
        self.des = ft.TextField(**inactive_style, width=350, label="Désignation")
        self.unite = ft.TextField(**inactive_style, width=110, label="Unite",)
        self.num_bon = ft.TextField(**inactive_style, width=150, label="Numero",)
        self.blf = ft.TextField(**filter_style, width=150, label="BSM",)
        self.id_ref = ft.Text("", visible=False)
        self.qte = ft.TextField(**filter_style, width=90, label="Qte", input_filter=ft.NumbersOnlyInputFilter())
        self.imputation = ft.Dropdown(**drop_style, width=150, label="Imputation",)
        self.num_bon = ft.TextField(**inactive_style, width=150, label="Numero",)
        self.comm = ft.TextField(**filter_style, width=600, label="Commentaire",)

        self.new_fen = ft.Card(
            elevation=50, surface_tint_color="white", width=600, height=630,
            left=(self.ctpr.page.window_width / 2) - 500, top=0,
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
                                ft.Text("nouvelle sortie".upper(), size=16, font_family="Poppins Regular"),
                            ], alignment="spaceBetween"
                        ),
                        ft.Divider(height=1, color="transparent"),
                        ft.Row(
                            controls=[
                                self.num_bon,
                                ft.Row([self.bt_select_date, self.sel_date])
                            ]
                        ),
                        ft.Row([self.blf, self.search_ref]),
                        ft.Container(
                            expand=True, padding=ft.padding.only(10, 3, 10, 3), height=100,
                            border_radius=8, border=ft.border.all(1, "#ebebeb"),
                            content=ft.Column(
                                expand=True, scroll="auto", height=150,
                                controls=[self.new_ref_table],
                            )
                        ),
                        ft.Divider(height=1, color="transparent"),
                        ft.Row(
                            [self.ref, self.des, self.id_ref]
                        ),
                        ft.Row([self.qte, self.imputation]),
                        self.comm,

                        ft.Divider(height=1, color="transparent"),
                        ft.ElevatedButton(
                            bgcolor='#3a5799', height=40,
                            style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=16)),
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.icons.CHECK, size=16, color="white"),
                                    ft.Text("Valider", size=12, color="white")
                                ], alignment='center'
                            ), on_click=self.creer_sortie
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
        # ...
        self.det_bon = ft.TextField(**filter_style, width=160, label="Numéro")
        self.det_bl = ft.TextField(**filter_style, width=250, label="BL Fournisseur")
        self.det_date = ft.TextField(**filter_style, width=140, label="date", prefix_icon="edit_calendar")
        self.det_ref = ft.TextField(**filter_style, width=250, label="Référence")
        self.det_des = ft.TextField(**filter_style, width=500, label="Désignation")
        self.det_qte = ft.TextField(**filter_style, width=80, label="Qté")
        self.det_imputation = ft.TextField(**filter_style, width=170, label="Imputation", prefix_icon=ft.icons.CREDIT_CARD)
        self.det_comm = ft.TextField(**filter_style, width=450, label="Commentaire")
        self.det_unite = ft.TextField(**filter_style, width=80, label="Unité")

        self.details_fen = ft.Card(
            elevation=50, surface_tint_color="white", width=600, height=470,
            left=(self.ctpr.page.window_width / 2) - 550, top=0,
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
                                ft.Text("Details bon".upper(), size=16, font_family="Poppins Regular"),
                            ], alignment="spaceBetween"
                        ),
                        ft.Divider(height=2, thickness=1),
                        ft.Divider(height=1, color="transparent"),
                        ft.Container(
                            padding=10, border_radius=8, border=ft.border.all(1, "#ebebeb"),
                            content=ft.Column(
                                controls=[
                                    ft.Row(controls=[self.det_bon, self.det_bl]),
                                    ft.Row([self.det_date, self.det_ref]),
                                    self.det_des,
                                    ft.Row([self.det_qte, self.det_unite, self.det_imputation,]),
                                    self.det_comm,
                                ], spacing=20
                            )
                        ),

                        ft.Divider(height=1, color="transparent"),
                        ft.ElevatedButton(
                            bgcolor='#3a5799', height=40,
                            style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=16)),
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.icons.CLOSE, size=16, color="white"),
                                    ft.Text("Quitter", size=12, color="white")
                                ], alignment='center'
                            ), on_click=self.close_details_fen
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
                    ft.Text("Sorties".upper(), size=20, font_family="Poppins Light"),
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
                                            tooltip='Exporter la vue excel',
                                            on_click=lambda _: self.ctpr.fp_extraire_sorties_vue.save_file(
                                                allowed_extensions=['xlsx'])
                                        ),
                                        ft.IconButton(
                                            ft.icons.FILE_UPLOAD_OUTLINED, icon_size=22, icon_color="#17274f",
                                            tooltip="Exporter toutes les entrées excel",
                                            on_click=lambda _: self.ctpr.fp_extraire_sorties.save_file(
                                                allowed_extensions=['xlsx'])
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
                self.new_fen, self.details_fen
            ]
        )
        self.ctpr.dp_new_sortie.on_change = self.change_date
        self.ctpr.fp_extraire_sorties.on_result = self.extraire_sorties
        self.ctpr.fp_extraire_sorties_vue.on_result = self.extraire_sorties_vue
        self.load_datas()

    def load_datas(self):
        for row in self.table.rows[:]:
            self.table.rows.remove(row)

        stock = be.all_sorties()

        for item in stock:
            self.table.rows.append(
                ft.DataRow(
                    data=item,
                    cells=[
                        ft.DataCell(ft.Text(item['numero'])),
                        ft.DataCell(ft.Text(item['date'])),
                        ft.DataCell(ft.Text(item['ref'])),
                        ft.DataCell(ft.Text(item['des'])),
                        ft.DataCell(ft.Text(item['qte'])),
                        ft.DataCell(ft.Text(item['imputation'])),
                    ], on_select_changed=self.select_ref
                )
            )

        # table de recherche
        all_refs = be.all_ref_name()

        for row in self.new_ref_table.rows[:]:
            self.new_ref_table.rows.remove(row)

        for item in all_refs:
            self.new_ref_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item[0])),
                        ft.DataCell(ft.Text(item[1])),
                    ],
                    on_select_changed=lambda e: self.select_new_ref(
                        e.control.cells[0].content.value,
                        e.control.cells[1].content.value,
                    )
                )
            )

        for imput in be.all_imputations_name():
            self.imputation.options.append(
                ft.dropdown.Option(imput)
            )

    def filter_datas(self, e):

        stock = be.all_sorties()
        filtre = self.filter.value.lower()

        if filtre is None or filtre == "":
            self.load_datas()
            self.table.update()

        else:
            for row in self.table.rows[:]:
                self.table.rows.remove(row)

            filter_datas = list(filter(lambda x: filtre in x['ref'].lower() or filtre in x['des'].lower(), stock))

            for item in filter_datas:
                self.table.rows.append(
                    ft.DataRow(
                        data=item,
                        cells=[
                            ft.DataCell(ft.Text(item['numero'])),
                            ft.DataCell(ft.Text(item['date'])),
                            ft.DataCell(ft.Text(item['ref'])),
                            ft.DataCell(ft.Text(item['des'])),
                            ft.DataCell(ft.Text(item['qte'])),
                            ft.DataCell(ft.Text(item['imputation'])),
                        ], on_select_changed=self.select_ref
                    )
                )

            self.table.update()

    def open_new_fen(self, e):
        self.new_fen.scale = 1
        self.new_fen.update()

    def close_new_fen(self, e):
        self.new_fen.scale = 0
        self.new_fen.update()

    def filter_ref(self, e):
        filtre = self.search_ref.value
        datas = be.all_ref_name()

        refs = [{'ref': row[0], 'des': row[1]} for row in datas]

        if filtre is None or filtre == "":
            self.load_datas()
            self.new_ref_table.update()

        else:
            filter_datas = list(filter(lambda x: filtre in x['ref'] or filtre in x['des'], refs))

            for row in self.new_ref_table.rows[:]:
                self.new_ref_table.rows.remove(row)

            for item in filter_datas:
                self.new_ref_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(item['ref'])),
                            ft.DataCell(ft.Text(item['des'])),
                        ],
                        on_select_changed=lambda e: self.select_new_ref(
                            e.control.cells[0].content.value,
                            e.control.cells[1].content.value,
                        )
                    )
                )

            self.new_ref_table.update()

    def select_ref(self, e):
        donnees = e.control.data

        self.det_bon.value = donnees['numero']
        self.det_bl.value = donnees['bon']
        self.det_date.value = donnees['date']
        self.det_ref.value = donnees['ref']
        self.det_des.value = donnees['des']
        self.det_qte.value = donnees['qte']
        self.det_comm.value = donnees['comm']
        self.det_imputation.value = donnees['imputation']
        self.det_unite.value = donnees['unite']

        for widget in (self.det_bon, self.det_bl, self.det_date, self.det_ref, self.det_des,
                       self.det_qte, self.det_imputation, self.det_comm, self.det_unite):
            widget.update()

        self.details_fen.scale = 1
        self.details_fen.update()

    def select_new_ref(self, e, f):
        self.ref.value = e
        self.des.value = f
        self.ref.update()
        self.des.update()

        self.id_ref.value = be.find_article_id_by_ref(self.ref.value)
        self.id_ref.update()

        self.num_bon.value = be.find_numero_bon_sortie()
        self.num_bon.update()

    def creer_sortie(self, e):
        count = 0
        for widget in (self.qte, self.imputation, self.blf, self.sel_date):
            if widget.value is None or widget.value == "":
                count += 1

        if count == 0:
            id_ref = int(self.id_ref.value)
            qte = int(self.qte.value)
            comm = "" if self.comm.value is None else self.comm.value

            stock_actu = be.stock_by_id(id_ref)
            nouveau_stock = stock_actu - qte

            if nouveau_stock < 0:
                self.ctpr.title_box.value = "Erreur"
                self.ctpr.title_box.update()
                self.ctpr.message.value = "Opération impossible, stock négatif"
                self.ctpr.message.update()
                self.ctpr.box.open = True
                self.ctpr.box.update()

            else:
                be.add_sortie(
                    self.num_bon.value, self.blf.value, self.sel_date.value, self.imputation.value,
                    id_ref, qte, comm
                )
                be.update_stock(nouveau_stock, id_ref)
                be.add_mouvement('S', self.num_bon.value, id_ref, stock_actu, nouveau_stock, qte)

            for widget in (self.blf, self.sel_date, self.num_bon, self.qte, self.imputation, self.comm, self.search_ref):
                widget.value = None
                widget.update()

            self.ctpr.title_box.value = "Validé"
            self.ctpr.title_box.update()
            self.ctpr.message.value = "Bon enregistré"
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

    def change_date(self, e):
        self.sel_date.value = str(self.ctpr.dp_new_sortie.value)[0:10]
        self.sel_date.update()

    def close_details_fen(self, e):
        self.details_fen.scale = 0
        self.details_fen.update()

    def extraire_sorties(self, e):
        table_datas = be.all_sorties()

        numeros = [row['numero'] for row in table_datas]
        bons = [row['bon'] for row in table_datas]
        dates = [row['date'] for row in table_datas]
        refs = [row['ref'] for row in table_datas]
        desigs = [row['des'] for row in table_datas]
        qtes = [row['qte'] for row in table_datas]
        unites = [row['unite'] for row in table_datas]
        imputations = [row['imputation'] for row in table_datas]
        comms = [row['comm'] for row in table_datas]

        entrees = {
            'date': dates, 'numero': numeros, 'bon livraison': bons, 'référence': refs,
            'désignation': desigs, 'unité': unites, 'quantité': qtes,
            'imputation': imputations, 'commentaire': comms
        }
        df = pandas.DataFrame(entrees)
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

    def extraire_sorties_vue(self, e):
        all_datas = be.all_sorties()

        filtre = self.filter.value.lower()

        if filtre is None or filtre == "":
            self.ctpr.title_box.value = "Erreur"
            self.ctpr.title_box.update()
            self.ctpr.message.value = "Aucun filtre détecté"
            self.ctpr.message.update()
            self.ctpr.box.open = True
            self.ctpr.box.update()

        else:
            table_datas = list(filter(lambda x: filtre in x['ref'].lower() or filtre in x['des'].lower(), all_datas))

            numeros = [row['numero'] for row in table_datas]
            bons = [row['bon'] for row in table_datas]
            dates = [row['date'] for row in table_datas]
            refs = [row['ref'] for row in table_datas]
            desigs = [row['des'] for row in table_datas]
            qtes = [row['qte'] for row in table_datas]
            unites = [row['unite'] for row in table_datas]
            imputations = [row['imputation'] for row in table_datas]
            comms = [row['comm'] for row in table_datas]

            entrees = {
                'date': dates, 'numero': numeros, 'bon livraison': bons, 'référence': refs,
                'désignation': desigs, 'unité': unites, 'quantité': qtes,
                'imputation': imputations, 'commentaire': comms
            }
            df = pandas.DataFrame(entrees)
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

