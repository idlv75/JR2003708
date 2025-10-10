"""runner.py — Executes the full Knight Journey workflow from the command line.

This module is responsible for connecting all the high-level components of the
Knight Journey program:

1. Parsing command-line arguments (input file path)
2. Reading and validating the YAML input file
3. Selecting the appropriate solving strategy
4. Running the journey computation
5. Printing formatted results to stdout

It also provides a `Runner` alias for backward compatibility so that
`from knight_journey.cli.runner import Runner` works for both scripts and tests.
"""

import argparse
import sys
from ..journey import Journey
from .parser import InputParser
from .strategy_selector import StrategySelector
from .validator import PreflightValidator
import logging
logger = logging.getLogger(__name__)


class JourneyRunner:
    """
    Coordinates the entire command-line execution flow for Knight Journey.

    Responsibilities:
    - Parse command-line arguments (`--input`)
    - Load and validate the YAML input
    - Select an execution strategy
    - Execute the journey computation
    - Output results in a strict, testable format

    Example usage:
    ---------------
    ```bash
    python -m knight_journey --input input.yaml
    ```
    """

    def __init__(self) -> None:
        """Initialize the argument parser and parse CLI arguments."""
        ap = argparse.ArgumentParser(description="Knight Journey - YAML input")
        ap.add_argument(
            "-i", "--input",
            required=True,
            help="Path to YAML file describing the game setup"
        )
        # Store parsed CLI arguments
        self.args = ap.parse_args()

    def run(self) -> None:
        """Run the full knight journey process and print results or errors."""
        logger.info(f"Starting Knight Journey with input: {self.args.input}")
        
        try:
            # Step 1: Parse input YAML file into structured data
            logger.debug("Parsing input file...")
            cells, n, max_g = InputParser(self.args.input).parse()
            logger.debug(f"Parsed {len(cells)} cells, n={n}, max_gold={max_g}")
        except FileNotFoundError:
            print("Error: Input file not found", file=sys.stderr)
            print(-1)
            return
        except yaml.YAMLError as e:
            print(f"Error: Invalid YAML syntax: {e}", file=sys.stderr)
            print(-1)
            return
        except (KeyError, ValueError, TypeError) as e:
            print(f"Error: Invalid data format: {e}", file=sys.stderr)
            print(-1)
            return
        except Exception as e:
            # Catch-all for unexpected errors
            print(f"Error: {e}", file=sys.stderr)
            print(-1)
            return

        # Step 2: Validate preconditions (e.g., grid size, cell data)
        logger.debug("Validating input data...")
        err = PreflightValidator.validate(cells, n)
        if err is not None:
            logger.warning(f"Validation failed: {err}")
            print(-1)
            return
        logger.debug("Validation passed")

        try:
            # Step 3: Choose solving strategy dynamically (e.g., heap/bucket)
            logger.debug("Selecting optimal strategy...")
            strategy = StrategySelector(n=n, max_gold=max_g).choose()
            logger.info(f"Using strategy: {strategy.__class__.__name__}")

            # Step 4: Execute the journey using the chosen strategy
            logger.debug("Executing journey...")
            result = Journey(cells, strategy).run()
            if result is None:
                # Indicates that no valid journey was found
                logger.info("No valid journey found")
                print(-1)
                return

            # Step 5: Format and print the result as expected by test suite
            total, positions = result
            logger.info(f"Journey successful: total_gold={total}, kills={len(positions)}")
            print(total)                       # Total score or gold
            print(len(positions))               # Number of positions visited
            print(" ".join(map(str, positions)) if positions else "")
        except Exception as e:
            # Catch any runtime errors during execution
            logger.error(f"Execution failed: {e}", exc_info=True)
            print(f"Error during execution: {e}", file=sys.stderr)
            print(-1)
            return


# ---------------------------------------------------------------------
# Compatibility alias for __main__.py and legacy tests
# ---------------------------------------------------------------------
Runner = JourneyRunner  # allows: from knight_journey.cli.runner import Runner

__all__ = ["JourneyRunner", "Runner"]
