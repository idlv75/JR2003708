## Dragons & Princesses (#548) - Hadar Balzam

Input is a YAML file that lists cells 2..n; output is three lines:

maximum total gold

number of dragons killed

their (1-based) indices in increasing order

If the plan is impossible, the program prints -1.

## How to run

```bash
pip install -r requirements.txt
python -m src.solver example.yaml
```
or

```bash
pip install -r requirements.txt
python src/solver.py example.yaml
```

## YAML Format
```yaml
n: 6
cells:
  - d 10
  - d 12
  - p 2
  - d 1
  - p 2

```
 ## Solution Approach
Greedy with a min-heap of chosen dragons (gold, idx):

Walk cells left→right.

Dragon: tentatively take it (push to heap).

Intermediate princess with beauty b: must have strictly fewer than b kills now.
→ While len(heap) ≥ b, pop the cheapest dragons.

Final princess (cell n) with beauty b_n: require len(heap) ≥ b_n; otherwise print -1.

Why optimal? When we must reduce kills, removing the lowest-gold dragons preserves maximum total.
Complexity: O(n log n) time, O(n) space.

## Project layout
```graphql
.
├─ SOLUTION.md
├─ example.yaml
├─ src/
│  ├─ models.py     # Cell (tiny container)
│  ├─ io_yaml.py    # parse_yaml(path) -> (n, [Cell])
│  ├─ planner.py    # compute_plan(n, cells) -> (total, indices)
│  └─ solver.py     # CLI: parse + plan + print 
└─ tests/
   ├─ data/
   │  ├─ ex_ok.yaml
   │  ├─ ex_impossible.yaml
   │  ├─ ex_many_princesses.yaml
   │  ├─ ex_all_dragons_ok.yaml
   │  └─ ex_early_strict.yaml
   ├─ test_planner.py        
   ├─ test_integration.py     
   └─ test_batch_cases.py    
```
## Tests
```bash
pytest -q
```