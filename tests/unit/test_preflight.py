from knight_journey.cli.validator import PreflightValidator
from knight_journey.domain import DragonCell, PrincessCell

def test_preflight_missing_last_princess():
    cells = [DragonCell(idx=2, gold=5)]
    err = PreflightValidator.validate(cells, n=3)
    assert err is not None

def test_preflight_last_beauty_too_large():
    cells = [
        DragonCell(idx=2, gold=1),
        PrincessCell(idx=3, beauty=1),
        PrincessCell(idx=6, beauty=5, is_last=True),
    ]
    err = PreflightValidator.validate(cells, n=6)
    assert err is not None

def test_preflight_no_dragons_but_last_needs_kills():
    cells = [
        PrincessCell(idx=3, beauty=1),
        PrincessCell(idx=4, beauty=1, is_last=True),
    ]
    err = PreflightValidator.validate(cells, n=4)
    assert err is not None

def test_preflight_mid_princess_invalid_beauty():
    cells = [
        PrincessCell(idx=2, beauty=0),
        PrincessCell(idx=5, beauty=0, is_last=True),
    ]
    err = PreflightValidator.validate(cells, n=5)
    assert err is not None

def test_preflight_ok_case():
    cells = [
        DragonCell(idx=2, gold=3),
        PrincessCell(idx=3, beauty=2),
        DragonCell(idx=4, gold=5),
        PrincessCell(idx=5, beauty=1, is_last=True),
    ]
    err = PreflightValidator.validate(cells, n=5)
    assert err is None
