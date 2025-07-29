import flet as ft
from src import CambioExactoApp


if __name__ == "__main__":
    app = CambioExactoApp()
    ft.app(target=app.create_app)
