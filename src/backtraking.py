from typing import List, Dict, Any


def backtrack_cambio_exacto(
    denominations: List[int],
    limits: List[int],
    target_amount: int
) -> Dict[str, Any]:
    """
    Algoritmo de backtracking optimizado para el problema de cambio exacto.
    Cuando encuentra una solución válida, no explora denominaciones restantes.
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
            'status': 'explorando'
        })

        # Caso base 1: Suma excede el objetivo (poda)
        if current_sum > target_amount:
            steps.append({
                'pos': pos,
                'current_sum': current_sum,
                'combination': list(current_combination),
                'status': 'podado'
            })
            return

        # Caso base 2: Suma exacta encontrada
        if current_sum == target_amount:
            # Completar la combinación con ceros para las denominaciones restantes
            complete_combination = list(current_combination)
            for i in range(pos, num_denominations):
                complete_combination[i] = 0
            
            solutions.append({
                'combination': complete_combination,
                'sum': current_sum
            })
            steps.append({
                'pos': pos,
                'current_sum': current_sum,
                'combination': complete_combination,
                'status': 'solución'
            })
            return

        # Caso base 3: Llegamos al final sin encontrar solución
        if pos == num_denominations:
            steps.append({
                'pos': pos,
                'current_sum': current_sum,
                'combination': list(current_combination),
                'status': 'rama muerta'
            })
            return

        # Explorar posibles cantidades para la denominación actual
        for i in range(limits[pos] + 1):
            current_combination[pos] = i
            new_pos = pos + 1
            new_sum = current_sum + i * denominations[pos]
            _backtrack(new_pos, new_sum)

    _backtrack(0, 0)
    return {
        'solutions': solutions,
        'steps': steps
    }
