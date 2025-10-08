# src/models.py
class Cell:
    """Tiny container for a single cell on the path.
    - idx: 1-based index (2..n from input)
    - kind: 'd' (dragon) or 'p' (princess)
    - value: gold (dragon) or beauty (princess)
    """
    def __init__(self, idx, kind, value):
        self.idx = idx
        self.kind = kind
        self.value = value