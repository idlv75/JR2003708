#
import sys

def main():
    data = sys.stdin
    line = data.readline().split()
    if not line:
        return
    n = int(line[0])

    cells = []
    princess_positions = []
    for i in range(2, n + 1):
        typ, val = data.readline().split()
        val = int(val)
        cells.append((i, typ, val))
        if typ == 'p':
            princess_positions.append((i, val))

    m = len(princess_positions)  
    if m == 0:
        print(-1)
        return

    # Record beauties
    beauties = [b for (_, b) in princess_positions]

    
    tasks_early = []  
    tasks_final = []  
    seg_idx = 1
    p_ptr = 0
    for (idx, typ, val) in cells:
        if typ == 'p':
            seg_idx += 1
            p_ptr += 1
            continue
        # Dragon
        g = val
        if seg_idx < m:
            tasks_early.append((g, idx, seg_idx))
        else:
            tasks_final.append((g, idx))

   
    c = [0] * m
    if m > 1:
        temp = [0] * (m - 1)
        temp[m - 2] = max(0, beauties[m - 2] - 1)
        for j in range(m - 3, -1, -1):
            v = max(0, beauties[j] - 1)
            temp[j] = min(v, temp[j + 1])
        for j in range(m - 1):
            c[j] = temp[j]

 
    max_cap = c[m - 2] if m > 1 else 0
    total_final = len(tasks_final)
    if max_cap + total_final < beauties[m - 1]:
        print(-1)
        return


    selected_early = []
    gold_early = 0
    if max_cap > 0 and tasks_early:
        tasks_early.sort(key=lambda x: (-x[0], x[1]))
        parent = list(range(max_cap + 1))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for g, pos, seg in tasks_early:
            d_cap = c[seg - 1]
            if d_cap <= 0:
                continue
            slot = find(d_cap)
            if slot == 0:
                continue
            parent[slot] = slot - 1
            selected_early.append(pos)
            gold_early += g

   
    selected_final = [pos for (g, pos) in tasks_final]
    gold_final = sum(g for (g, pos) in tasks_final)

    kills = len(selected_early) + len(selected_final)
    if kills < beauties[m - 1]:
        print(-1)
        return

    total_gold = gold_early + gold_final
    print(total_gold)
    print(kills)
    result_positions = selected_early + selected_final
    result_positions.sort()
    print(" ".join(str(p) for p in result_positions))

if __name__ == '__main__':
    main()
