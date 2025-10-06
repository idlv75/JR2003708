# Core logic for Dragons & Princesses
from typing import Any, Dict, List, Tuple
import heapq


def solve_cells(data: Dict[str, Any]) -> Tuple[int, List[int]]:
    # read
    n = data.get("n")
    cells = data.get("cells")

    # validation
    if not isinstance(n, int):
        raise ValueError("n must be an integer.")
    if not (2 <= n <= 2 * 10**5):
        raise ValueError("n is out of range [2..200000].")
    if not isinstance(cells, list):
        raise ValueError("'cells' must be a list.")
    if len(cells) != n:
        raise ValueError("len(cells) must equal n.")
    if not cells or cells[-1].get("type") != "p":
        raise ValueError("last cell must be a princess (type: p).")

    # min-heap of (gold, cell_no)
    heap: List[Tuple[int, int]] = []
    gold_sum = 0

    # process cells[1..n-1] (cell 1 is start/empty)
    for i in range(1, n):
        ev = cells[i]
        t = ev.get("type")

        if t == "d":
            g = ev.get("g")
            if not isinstance(g, int):
                raise ValueError(f"cell {i+1}: dragon 'g' must be int.")
            if not (1 <= g <= 10**4):
                raise ValueError(f"cell {i+1}: dragon 'g' out of range [1..10000].")
            heapq.heappush(heap, (g, i + 1))  # cell_no = i+1
            gold_sum += g

        elif t == "p":
            b = ev.get("b")
            if not isinstance(b, int):
                raise ValueError(f"cell {i+1}: princess 'b' must be int.")
            if not (1 <= b <= 2 * 10**5):
                raise ValueError(f"cell {i+1}: princess 'b' out of range [1..200000].")

            is_final = (i == n - 1)
            if is_final:
                # final - need at least b slain
                if len(heap) < b:
                    return -1, []
            else:
                # non final - keep slain < b
                # pop cheapest until condition holds
                while len(heap) >= b and heap:
                    g_pop, _ = heapq.heappop(heap)
                    gold_sum -= g_pop

        else:
            raise ValueError(f"cell {i+1}: type must be 'd' or 'p'.")

    # collect kept dragon indices
    kept_indices = sorted(idx for _, idx in heap)
    return gold_sum, kept_indices
