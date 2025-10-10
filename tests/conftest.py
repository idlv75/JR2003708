# Shared utilities/fixtures for tests.
def yaml_text(cells, n=None):
    """Build YAML text from tuples: [('d',10), ('p',2), ...]."""
    if n is None:
        n = 1 + len(cells)
    lines = [f"n: {n}", "cells:"]
    for t, v in cells:
        if t == "d":
            lines.append(f"  - type: d\n    gold: {v}")
        else:
            lines.append(f"  - type: p\n    beauty: {v}")
    return "\n".join(lines) + "\n"
