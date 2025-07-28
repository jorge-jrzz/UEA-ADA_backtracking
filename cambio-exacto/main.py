import flet as ft

from create_coin import create_coin
from backtraking import backtrack_cambio_exacto


class CambioExactoVisualApp:
    def __init__(self):
        self.denominations = []
        self.limits = []
        self.target_amount = 0
        self.num_denominations = 0
        self.current_combination = []
        self.solutions = []
        self.min_coins_solution = None
        self.min_coins_count = float('inf')
        
        # Componentes para visualización del árbol
        self.current_path = []
        self.step_counter = 0
        
        # Componentes de la UI
        self.denominations_input = None
        self.limits_input = None
        self.target_input = None
        self.solutions_container = None
        self.best_solution_container = None
        self.tree_container = None
        self.step_counter_text = None
        self.animation_controls = None
        self.coins_display = None

    def update_coins_display(self):
        """Actualiza la visualización de las monedas disponibles."""
        if not self.denominations:
            return   
        coins_row = ft.Row(
            controls=[],
            alignment=ft.MainAxisAlignment.CENTER,
            wrap=True,
        )
        for _, (denom, limit) in enumerate(zip(self.denominations, self.limits)):
            coin_container = ft.Container(
                content=ft.Column([
                    create_coin(denom),
                    ft.Text(f"Límite: {limit}", size=12, text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                margin=ft.margin.all(10),
            )
            coins_row.controls.append(coin_container)
        self.coins_display.content = coins_row
        self.page.update()

    def update_solutions_display(self):
        """Actualiza la visualización de las soluciones."""
        self.solutions_container.controls.clear()
        if not self.solutions:
            self.solutions_container.controls.append(
                ft.Container(
                    content=ft.Text(
                        "No se encontraron soluciones",
                        size=16,
                        color=ft.Colors.RED_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(20),
                )
            )
        else:
            for idx, sol in enumerate(self.solutions):
                solution_coins = ft.Row(
                    controls=[],
                    alignment=ft.MainAxisAlignment.CENTER,
                    wrap=True,
                )
                for i, count in enumerate(sol['combination']):
                    if count > 0:
                        solution_coins.controls.append(
                            create_coin(self.denominations[i], count, True)
                        )
                solution_card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"Solución {idx + 1}", weight=ft.FontWeight.BOLD),
                            solution_coins,
                            ft.Text(f"Total: {sol['sum']}", size=14),
                            ft.Text(f"Monedas usadas: {sum(sol['combination'])}", size=12),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=ft.padding.all(15),
                    ),
                    margin=ft.margin.symmetric(vertical=5, horizontal=5),
                )
                self.solutions_container.controls.append(solution_card)

    def update_best_solution_display(self):
        """Actualiza la visualización de la mejor solución."""
        self.best_solution_container.controls.clear()
        if self.min_coins_solution:
            best_coins = ft.Row(
                controls=[],
                alignment=ft.MainAxisAlignment.CENTER,
                wrap=True,
            )
            for i, count in enumerate(self.min_coins_solution['combination']):
                if count > 0:
                    best_coins.controls.append(
                        create_coin(self.denominations[i], count, True)
                    )
            best_card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "🏆 Mejor solución",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.AMBER_700,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        best_coins,
                        ft.Text(
                            f"Total: {self.min_coins_solution['sum']}",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            f"Monedas mínimas: {self.min_coins_count}",
                            size=14,
                            color=ft.Colors.GREEN_600,
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.padding.all(20),
                ),
                color=ft.Colors.AMBER_50,
            )
            self.best_solution_container.controls.append(best_card)

    def process_input(self, e):
        """Procesa la entrada y ejecuta el algoritmo."""
        # Limpiar resultados anteriores
        self.solutions.clear()
        self.min_coins_solution = None
        self.min_coins_count = float('inf')
        self.current_path.clear()
        self.step_counter = 0
        # Limpiar displays
        self.solutions_container.controls.clear()
        self.best_solution_container.controls.clear()
        self.step_counter_text.value = "Pasos: 0"
        
        self.denominations = list(map(int, self.denominations_input.value.split()))
        self.limits = list(map(int, self.limits_input.value.split()))
        self.target_amount = int(self.target_input.value)

        # lanzar_visualizador()

        self.num_denominations = len(self.denominations)
        self.current_combination = [0] * self.num_denominations

        # Actualizar visualización de monedas
        self.update_coins_display()

        # Mostrar mensaje de procesamiento
        self.solutions_container.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.ProgressRing(width=20, height=20),
                    ft.Text("Procesando... Ejecutando backtracking", size=16),
                ], alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.padding.all(20),
            )
        )
        self.page.update()

        # Ejecutar algoritmo universal
        result = backtrack_cambio_exacto(self.denominations, self.limits, self.target_amount)
        self.solutions = result['solutions']
        self.step_counter = len(result['steps'])

        # Buscar mejor solución
        self.min_coins_count = float('inf')
        self.min_coins_solution = None
        for sol in self.solutions:
            total_coins = sum(sol['combination'])
            if total_coins < self.min_coins_count:
                self.min_coins_count = total_coins
                self.min_coins_solution = sol

        # Actualizar contadores y displays
        self.step_counter_text.value = f"Pasos ejecutados: {self.step_counter}"
        self.update_solutions_display()
        self.update_best_solution_display()
        
        self.page.update()

    def clear_all(self, e):
        """Limpia todos los campos y resultados."""
        self.denominations_input.value = ""
        self.limits_input.value = ""
        self.target_input.value = ""
        self.solutions_container.controls.clear()
        self.best_solution_container.controls.clear()
        self.coins_display.content = ft.Container()
        self.step_counter_text.value = "Pasos: 0"
        self.page.update()

    def load_example(self, e):
        """Carga un ejemplo predefinido."""
        self.denominations_input.value = "1 3 4 5"
        self.limits_input.value = "5 2 2 1"
        self.target_input.value = "7"
        self.page.update()

    def main(self, page: ft.Page):
        self.page = page
        page.title = "🪙 Cambio exacto - Algoritmo Backtracking"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window.maximized = True
        page.scroll = ft.ScrollMode.AUTO
        page.padding = 20
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Crear componentes de UI
        self.denominations_input = ft.TextField(
            label="Denominaciones (ej: 1 3 4 5)",
            width=350,
            prefix_icon=ft.Icons.MONETIZATION_ON_OUTLINED,
        )
        
        self.limits_input = ft.TextField(
            label="Límites por moneda (ej: 5 2 2 1)",
            width=350,
            prefix_icon=ft.Icons.NUMBERS,
        )
        
        self.target_input = ft.TextField(
            label="Cantidad",
            width=200,
            prefix_icon=ft.Icons.RADAR,
        )

        # Botones de control
        controls_row = ft.Row([
            ft.ElevatedButton(
                "Buscar soluciones",
                on_click=self.process_input,
                bgcolor=ft.Colors.BLUE_600,
                color=ft.Colors.WHITE,
                icon=ft.Icons.SEARCH,
            ),
            ft.OutlinedButton(
                "Cargar ejemplo",
                on_click=self.load_example,
                icon=ft.Icons.LIGHTBULB_OUTLINE,
            ),
            ft.OutlinedButton(
                "Limpiar",
                on_click=self.clear_all,
                icon=ft.Icons.CLEAR,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER)

        # Contenedores para resultados
        self.coins_display = ft.Container(
            content=ft.Text("Introduce las denominaciones para ver las monedas", 
                          text_align=ft.TextAlign.CENTER),
            padding=ft.padding.all(20),
        )

        self.solutions_container = ft.Row([], wrap=True, scroll=ft.ScrollMode.AUTO)
        self.best_solution_container = ft.Column([])
        
        self.step_counter_text = ft.Text("Pasos: 0", size=14, color=ft.Colors.GREY_600)

        # Layout principal
        page.add(
            ft.AppBar(
                title=ft.Text("🪙 Cambio exacto - Algoritmo Backtracking"),
                bgcolor=ft.Colors.BLUE_800,
                color=ft.Colors.WHITE,
            ),
            
            # Sección de entrada
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("🔧 Datos de entrada", 
                               size=20, weight=ft.FontWeight.BOLD),
                        ft.Row([
                            self.denominations_input,
                            self.limits_input,
                            self.target_input,
                        ], alignment=ft.MainAxisAlignment.CENTER, wrap=True),
                        controls_row,
                        self.step_counter_text,
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.padding.all(20),
                ),
                margin=ft.margin.symmetric(vertical=10),
            ),

            # Visualización de monedas
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("🪙 Monedas disponibles", 
                               size=18, weight=ft.FontWeight.BOLD),
                        self.coins_display,
                    ], horizontal_alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.padding.all(20),
                ),
                margin=ft.margin.symmetric(vertical=10)
            ),

            # Mejores soluciones
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("🎯 Resultado", size=18, weight=ft.FontWeight.BOLD),
                        self.best_solution_container,
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.padding.all(20),
                ),
                margin=ft.margin.symmetric(vertical=10),
            ),

            # Todas las soluciones
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("📋 Todas las soluciones", 
                               size=18, weight=ft.FontWeight.BOLD),
                        self.solutions_container,  # Ahora es un Row con wrap
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.padding.all(20),
                ),
                margin=ft.margin.symmetric(vertical=10),
            ),
        )

# Para ejecutar la aplicación
if __name__ == "__main__":
    app = CambioExactoVisualApp()
    ft.app(target=app.main)