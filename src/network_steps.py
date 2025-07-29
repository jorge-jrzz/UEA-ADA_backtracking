import time
import argparse

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from backtraking import backtrack_cambio_exacto


ANIMATION_DELAY = 0.5           # Segundos entre pasos (0 = sin animación)
SHOW_STEP_BY_STEP = True        # True = muestra paso a paso, False = solo resultado final
COLOR_MAP = {
    'root': '#1565C0',
    'exploring': '#FF9800',
    'solution': '#4CAF50',
    'pruned': '#F44336',
    'dead_end': '#757575'
}


class BacktrackingTreeVisualizer:
    def __init__(self, denominations, limits, target):
        self.denominations = denominations
        self.limits = limits
        self.target_amount = target
        self.num_denominations = len(denominations)
        
        # Estructura del árbol
        self.tree_graph = nx.DiGraph()
        self.tree_history = []
        self.solutions = []
        self.step_counter = 0
        
        # Inicializar nodo raíz
        self.tree_graph.add_node('root', 
                               label='RAÍZ\nΣ=0', 
                               status='root',
                               level=0,
                               step=0)

        node_colors = []
        node_labels = []

    def process_steps(self, steps):
        """Procesa los pasos devueltos por backtrack_cambio_exacto y construye el árbol."""
        for idx, step in enumerate(steps):
            pos = step['pos']
            current_sum = step['current_sum']
            combination = step['combination']
            status = step['status']
            reason = step.get('reason', "")

            # Crear ID único para el nodo
            comb_id = "_".join([str(c) for c in combination[:pos]]) if pos > 0 else ""
            node_id = f"L{pos}_{comb_id}" if comb_id else f"step_{idx}"

            # Determinar parent_id
            if pos > 0:
                parent_comb = combination[:pos-1]
                parent_id = f"L{pos-1}_" + "_".join([str(c) for c in parent_comb]) if parent_comb else 'root'
            else:
                parent_id = 'root'

            # Crear etiqueta del nodo
            if pos > 0 and pos <= len(self.denominations):
                denomination = self.denominations[pos-1]
                count = combination[pos-1] if pos-1 >= 0 else 0
                label = f"D{denomination}:{count}\nΣ={current_sum}"
            else:
                continue

            # Agregar nodo al grafo
            self.tree_graph.add_node(node_id,
                                   label=label,
                                   status=status,
                                   level=pos,
                                   step=idx,
                                   sum=current_sum)
            # Agregar arista desde el padre
            if parent_id in self.tree_graph.nodes():
                self.tree_graph.add_edge(parent_id, node_id)

            # Registrar en historial
            step_data = {
                'step': idx,
                'pos': pos,
                'current_sum': current_sum,
                'combination': list(combination),
                'status': status,
                'reason': reason,
                'node_id': node_id
            }
            self.tree_history.append(step_data)

            # Animación paso a paso
            if SHOW_STEP_BY_STEP and ANIMATION_DELAY > 0:
                self.visualize_current_tree(f"Paso {idx} - {status}")
                time.sleep(ANIMATION_DELAY)

    def run_backtracking(self):
        """Ejecuta el algoritmo completo y muestra el árbol."""
        
        if SHOW_STEP_BY_STEP:
            plt.ion()  # Modo interactivo para animación
            plt.figure(figsize=(16, 10))
            manager = plt.get_current_fig_manager()
            try:
                manager.full_screen_toggle()
            except Exception:
                pass

        result = backtrack_cambio_exacto(self.denominations, self.limits, self.target_amount)
        
        # Procesar pasos y soluciones
        self.process_steps(result['steps'])
        self.solutions = result['solutions']
        
        if SHOW_STEP_BY_STEP:
            plt.ioff()  # Desactivar modo interactivo
        
        # Mostrar árbol final
        self.visualize_final_tree()

    def hierarchical_layout(self):
        """Layout jerárquico para el árbol."""
        pos = {}
        levels = {}
        
        # Agrupar nodos por nivel
        for node in self.tree_graph.nodes():
            level = self.tree_graph.nodes[node]['level']
            if level not in levels:
                levels[level] = []
            levels[level].append(node)
        
        # Posicionar nodos
        for level, nodes in levels.items():
            y = -level * 1.8  # Separación vertical
            width = len(nodes)
            
            # Ordenar por paso para mantener orden de exploración
            sorted_nodes = sorted(nodes, key=lambda n: self.tree_graph.nodes[n]['step'])
            
            for i, node in enumerate(sorted_nodes):
                x = (i - width/2) * 3.0  # Separación horizontal
                pos[node] = (x, y)

        self.node_colors = [COLOR_MAP.get(self.tree_graph.nodes[node]['status'], '#CCCCCC')
                            for node in self.tree_graph.nodes()]
        self.node_labels = {node: self.tree_graph.nodes[node]['label']
                            for node in self.tree_graph.nodes()}

        return pos

    def _draw_tree(self, pos, node_colors, node_labels, node_size=2000, edge_width=1.5, edge_alpha=0.7, arrowsize=12, font_size=8):
        """Dibuja nodos, aristas y etiquetas del árbol."""
        nx.draw_networkx_edges(
            self.tree_graph, pos,
            edge_color='#444444',
            arrows=True, arrowsize=arrowsize,
            width=edge_width, alpha=edge_alpha
        )
        nx.draw_networkx_nodes(
            self.tree_graph, pos,
            node_color=node_colors,
            node_size=node_size, alpha=0.9,
            edgecolors='black', linewidths=2
        )
        nx.draw_networkx_labels(
            self.tree_graph, pos, node_labels,
            font_size=font_size, font_weight='bold', font_color='white'
        )

    def visualize_current_tree(self, title_suffix=""):
        """Visualiza el estado actual del árbol."""
        if not SHOW_STEP_BY_STEP:
            return

        plt.clf()  # Limpiar plot anterior

        pos = self.hierarchical_layout()

        self._draw_tree(pos, self.node_colors, self.node_labels)

        plt.title(
            f'Árbol de Backtracking - {title_suffix}\n'
            f'Objetivo: {self.target_amount} | Denominaciones: {self.denominations} | Límites: {self.limits}\n',
            fontsize=14, fontweight='bold'
        )
        plt.axis('off')
        plt.tight_layout()
        plt.pause(0.2)  # Pequeña pausa para actualizar

    def visualize_final_tree(self):
        """Visualización final del árbol completo."""
        plt.figure(figsize=(20, 14))
        plt.clf()

        pos = self.hierarchical_layout()

        self._draw_tree(pos, self.node_colors, self.node_labels)

        solutions_count = len([s for s in self.tree_history if s['status'] == 'solution'])
        pruned_count = len([s for s in self.tree_history if s['status'] == 'pruned'])
        dead_end_count = len([s for s in self.tree_history if s['status'] == 'dead_end'])

        plt.title(
            f'Cambio Exacto para {self.target_amount}\n'
            f'Denominaciones: {self.denominations} | Límites: {self.limits}\n'
            f'Pasos totales: {len(self.tree_history)}',
            fontsize=15, fontweight='bold'
        )

        legend_elements = [
            patches.Circle((0, 0), 0.1, facecolor='#1565C0', edgecolor='black', label='Raíz'),
            patches.Circle((0, 0), 0.1, facecolor='#FF9800', edgecolor='black', label='Explorando'),
            patches.Circle((0, 0), 0.1, facecolor='#4CAF50', edgecolor='black', label=f'Solución ✓ ({solutions_count})'),
            patches.Circle((0, 0), 0.1, facecolor='#F44336', edgecolor='black', label=f'Podado ✗ ({pruned_count})'),
            patches.Circle((0, 0), 0.1, facecolor='#757575', edgecolor='black', label=f'Sin solución ∅ ({dead_end_count})')
        ]

        plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.02, 0.98),
                   fontsize=12, frameon=True, fancybox=True, shadow=True)

        plt.axis('off')
        plt.tight_layout()
        plt.show()

def view_backtracking_tree(denominations: list[int], limits: list[int], target_amount: int) -> None:
    visualizer = BacktrackingTreeVisualizer(denominations, limits, target_amount)
    visualizer.run_backtracking()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualiza el árbol de backtracking para el problema de cambio exacto.")
    parser.add_argument('--denominations', nargs='+', type=int, required=True, help='Lista de denominaciones (ej: 1 3)')
    parser.add_argument('--limits', nargs='+', type=int, required=True, help='Lista de límites para cada denominación (ej: 2 3)')
    parser.add_argument('--target', type=int, required=True, help='Cantidad objetivo (ej: 6)')
    args = parser.parse_args()

    if len(args.denominations) != len(args.limits):
        raise ValueError("La cantidad de denominaciones y límites debe ser igual.")

    view_backtracking_tree(args.denominations, args.limits, args.target)
