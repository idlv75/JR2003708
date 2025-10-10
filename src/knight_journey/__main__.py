from __future__ import annotations
from knight_journey.cli.runner import JourneyRunner


def main() -> None:
    """
    Parse CLI args and run the journey. Always print either a valid result
    or '-1' per the test contract. Never crash; exit code should be 0.
    """
    # JourneyRunner parses its own args in __init__ and handles everything
    JourneyRunner().run()
    # Tests expect return code 0 even when we printed -1 (handled failure).
    # The runner handles all output internally.


if __name__ == "__main__":
    main()
