# Dragons and Princesses - CodeForces #548

Python solution for the dragons and princesses problem.

## Requirements

```bash
pip install -r requirements.txt
```

## Usage

```bash
python solution.py example1.yaml
```

## Run Tests

```bash
python -m unittest test_solution.py -v
```

## Solution

The knight needs to reach the last princess while maximizing gold. Intermediate princesses force marriage if too many dragons are killed before reaching them.

The solution uses frozen dataclasses for immutability and tries a greedy approach first (selecting highest-value dragons), then falls back to checking all combinations if the greedy approach violates princess constraints.
