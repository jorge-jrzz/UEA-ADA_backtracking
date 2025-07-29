import flet as ft


def create_coin(denomination: int, count: int = 1, is_selected: bool = False):
    """
    Crea un control visual mejorado que representa una moneda.
    """
    # Determinar el color basado en la denominación
    if denomination <= 1:
        color = ft.Colors.AMBER_500
        border_color = ft.Colors.AMBER_700
    elif denomination <= 5:
        color = ft.Colors.GREY_400
        border_color = ft.Colors.GREY_600
    elif denomination <= 10:
        color = ft.Colors.YELLOW_600
        border_color = ft.Colors.YELLOW_800
    elif denomination <= 25:
        color = ft.Colors.ORANGE_500
        border_color = ft.Colors.ORANGE_700
    else:
        color = ft.Colors.BLUE_GREY_400
        border_color = ft.Colors.BLUE_GREY_600

    # Cambiar apariencia si está seleccionada
    if is_selected:
        color = ft.Colors.GREEN_400
        border_color = ft.Colors.GREEN_700

    coin_content = ft.Column(
        [
            ft.Text(
                value=str(denomination),
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE,
            ),
            ft.Text(
                value=f"x{count}" if count > 1 else "",
                size=14,
                color=ft.Colors.WHITE70,
            ) if count > 0 else ft.Container()
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0
    )

    return ft.Container(
        width=80,
        height=80,
        content=coin_content,
        alignment=ft.alignment.center,
        bgcolor=color,
        border=ft.border.all(3, border_color),
        border_radius=ft.border_radius.all(40),
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=8,
            color=ft.Colors.BLACK26,
            offset=ft.Offset(2, 2),
        ),
        margin=ft.margin.all(5),
        animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
    )