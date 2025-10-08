# src/planner.py
import heapq

def compute_plan(n, cells):
    """Greedy:
    - Keep min-heap of chosen dragons (gold, idx).
    - On dragon: push (take it tentatively).
    - On intermediate princess with beauty b: enforce kills < b by popping cheapest.
    - On final princess with beauty b_n: require kills >= b_n, else raise ValueError("IMPOSSIBLE").
    Returns (total_gold, sorted_indices).
    """
    chosen = []      # (gold, idx)
    total_gold = 0

    for c in cells:
        if c.kind == "d": # dragon we will be greedy and add it to the minHEAP.
            heapq.heappush(chosen, (c.value, c.idx))
            total_gold += c.value
        else:
            beauty = c.value
            is_last = (c.idx == n) # cheeking if it is the last princess.

            if not is_last:
                while len(chosen) >= beauty: # this way we remove the dragon with the least amount of gold.
                    g, _i = heapq.heappop(chosen)
                    total_gold -= g
            else:
                if len(chosen) < beauty:
                    raise ValueError("IMPOSSIBLE") # if we got to the end and we don't have enough killed dragons so the mission is impossible.

    indices = sorted(idx for _, idx in chosen) # sorting the list.
    return total_gold, indices
