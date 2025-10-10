"""Input validation for Knight Journey.

This module validates all input data before processing to ensure:
- Data integrity
- Constraint satisfaction
- Prevention of runtime errors

Validation contract per tests in tests/unit/test_preflight.py
"""
from __future__ import annotations
from typing import List, Optional
from ..domain import DragonCell, PrincessCell, Cell
from ..config import ValidationConfig


class PreflightValidator:
    """Validates input data before journey execution.
    
    This class implements the Validator pattern to ensure all
    preconditions are met before attempting journey computation.
    """

    @staticmethod
    def validate(cells: List[Cell], n: int) -> Optional[str]:
        """Validate cells and board configuration.
        
        Args:
            cells: List of Cell objects representing the journey path
            n: Board size (expected position of last princess)
            
        Returns:
            None if validation passes, error message string otherwise
        """
        if not cells:
            return "missing last princess"

        # Check last princess existence & position/index
        last = cells[-1]
        if not isinstance(last, PrincessCell) or not getattr(last, "is_last", False):
            return "missing last princess"
        if getattr(last, "idx", None) != n:
            # Index of last princess must be exactly n
            return "missing last princess"

        total_dragons = 0

        for c in cells:
            if isinstance(c, DragonCell):
                # Validate dragon gold is non-negative
                if c.gold < ValidationConfig.MIN_GOLD:
                    return f"dragon gold must be non-negative at idx {c.idx}"
                # Validate dragon gold doesn't exceed maximum (prevents memory issues)
                if c.gold > ValidationConfig.MAX_GOLD:
                    return f"dragon gold exceeds maximum at idx {c.idx}"
                total_dragons += 1
            elif isinstance(c, PrincessCell):
                is_last = bool(getattr(c, "is_last", False))
                if not is_last:
                    # Mid princess beauty must be >=1
                    if c.beauty < ValidationConfig.MIN_BEAUTY_MID or c.beauty > ValidationConfig.MAX_BEAUTY_MID:
                        return f"princess beauty out of range at idx {c.idx}"
                else:
                    # Last princess beauty can be 0
                    if c.beauty < ValidationConfig.MIN_BEAUTY_LAST or c.beauty > ValidationConfig.MAX_BEAUTY_LAST:
                        return f"last princess beauty out of range at idx {c.idx}"
            else:
                return f"invalid cell type at idx {getattr(c, 'idx', '?')}"

        # Final feasibility: last princess requires at most total_dragons kills
        last_beauty = last.beauty  # type: ignore[attr-defined]
        if last_beauty > total_dragons:
            return "impossible: last princess requires more kills than total dragons"

        return None
