#!/usr/bin/env python3
# acmsguru #548 — Dragons and Princesses
#
# Input  : YAML file describing cells 2..n (each is a dragon or a princess)
# Output :
#   line 1: maximum total gold (or -1 if impossible)
#   line 2: k = number of dragons you kill
#   line 3: k increasing indices of those dragons
#
# How it works:
# - Walk left→right and keep a MIN-HEAP of dragons we plan to kill: (gold, idx).
# - Dragon → tentatively take it (push to heap).
# - Intermediate princess with beauty b → must have STRICTLY FEWER than b kills.
#   If we have too many, pop the CHEAPEST dragons first (they contribute least).
# - Final princess with beauty b_n → must end with AT LEAST b_n kills; else impossible.
#
# Greedy optimality: whenever a princess forces us to reduce kills, dropping the lowest-gold
# dragons maximizes the remaining total gold.
import os, sys
import argparse
try:
    from src.io_yaml import parse_yaml
    from src.planner import compute_plan
except ModuleNotFoundError:
    from io_yaml import parse_yaml
    from planner import compute_plan

def _main(argv):
    p = argparse.ArgumentParser(description="Solve 'Dragons and Princesses' from YAML.")
    p.add_argument("yaml_file", help="Path to input YAML.")
    args = p.parse_args(argv)

    try:
        n, cells = parse_yaml(args.yaml_file) #parsing the yaml file.
        total, indices = compute_plan(n, cells) # computing the solution.

        print(total)
        print(len(indices))
        print(*indices) if indices else print()
        return 0
    #errors handling.
    except ValueError as e:
        if str(e) == "IMPOSSIBLE":
            print(-1)
            return 0
        print(f"Error: {e}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))