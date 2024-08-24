import flet as ft
from pages.landing import Landing
from pages.accueil import Accueil
from pages.articles import Articles


def main(page: ft.Page):
    page.fonts = {
        "Poppins Regular": "fonts/Poppins-Regular.ttf",
        "Poppins Bold": "fonts/Poppins-Bold.ttf",
        "Poppins Black": "fonts/Poppins-Black.ttf",
        "Poppins Italic": "fonts/Poppins-Italic.ttf",
        "Poppins Medium": "fonts/Poppins-Medium.ttf",
        "Poppins ExtraBold": "fonts/Poppins-ExtraBold.ttf"
    }
    page.theme = ft.Theme(
        font_family="Poppins Medium"
    )

    def change_route(route):

        # initial route ...
        page.views.clear()
        page.views.append(Landing(page))
        page.update()

        if page.route == "/accueil":
            page.views.append(Accueil(page))
            page.update()

        if page.route == "/articles":
            page.views.append(Articles(page))
            page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.view[-1]
        page.go(top_view.route)

    page.on_route_change = change_route
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == '__main__':
    ft.app(target=main)

