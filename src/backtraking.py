from typing import List, Dict, Any


def backtrack_cambio_exacto(
    denominations: List[int],
    limits: List[int],
    target_amount: int
) -> Dict[str, Any]:
    """
    Algoritmo de backtracking universal para el problema de cambio exacto.
    Devuelve un diccionario con:
      - 'solutions': lista de soluciones encontradas
      - 'steps': lista de todos los pasos explorados (para visualización)
    """
    num_denominations = len(denominations)
    current_combination = [0] * num_denominations
    solutions = []
    steps = []

    def _backtrack(pos: int, current_sum: int):
        # Guardar paso explorado
        steps.append({
            'pos': pos,
            'current_sum': current_sum,
            'combination': list(current_combination),
            'status': 'exploring'
        })

        # Caso base 1: Suma excede el objetivo (poda)
        if current_sum > target_amount:
            steps.append({
                'pos': pos,
                'current_sum': current_sum,
                'combination': list(current_combination),
                'status': 'pruned'
            })
            return

        # Caso base 2: Llegamos al final
        if pos == num_denominations:
            if current_sum == target_amount:
                solutions.append({
                    'combination': list(current_combination),
                    'sum': current_sum
                })
                steps.append({
                    'pos': pos,
                    'current_sum': current_sum,
                    'combination': list(current_combination),
                    'status': 'solution'
                })
            else:
                steps.append({
                    'pos': pos,
                    'current_sum': current_sum,
                    'combination': list(current_combination),
                    'status': 'dead_end'
                })
            return

        # Explorar posibles cantidades para la denominación actual
        for i in range(limits[pos] + 1):
            current_combination[pos] = i
            _backtrack(pos + 1, current_sum + i * denominations[pos])

    _backtrack(0, 0)
    return {
        'solutions': solutions,
        'steps': steps
    }
