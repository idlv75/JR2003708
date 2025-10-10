# 🏛️ Architecture Documentation

## Table of Contents
- [Overview](#overview)
- [Design Patterns](#design-patterns)
- [Project Structure](#project-structure)
- [Core Components](#core-components)
- [Data Flow](#data-flow)
- [Algorithm Selection](#algorithm-selection)
- [Extension Points](#extension-points)

---

## Overview

Knight Journey is designed as a modular, extensible command-line application that solves an optimization problem using multiple strategies. The architecture follows SOLID principles and incorporates several design patterns.

### Key Characteristics

- **Modular** - Clear separation of concerns
- **Extensible** - Easy to add new strategies
- **Testable** - High test coverage with isolated components
- **Type-safe** - Full type hints for IDE support
- **Observable** - Comprehensive logging system

---

## Design Patterns

### 1. **Strategy Pattern** 🎯

**Location**: `src/knight_journey/strategy.py`, `strategies/`

**Purpose**: Encapsulate different algorithms (HeapStrategy, BucketsStrategy) behind a common interface.

```python
class KillingStrategy(ABC):
    @abstractmethod
    def on_dragon(self, gold: int, pos: int) -> None: ...
    @abstractmethod
    def enforce_before_princess(self, beauty: int) -> None: ...
```

**Benefits**:
- Algorithm can be selected at runtime
- Easy to add new strategies
- Strategies are interchangeable

---

### 2. **Factory Pattern** 🏭

**Location**: `src/knight_journey/cli/strategy_selector.py`

**Purpose**: Create strategy instances based on input characteristics.

```python
class StrategySelector:
    def choose(self) -> KillingStrategy:
        if nlogn < linear * threshold:
            return HeapStrategy(...)
        return BucketsStrategy(...)
```

**Benefits**:
- Centralized strategy creation logic
- Automatic selection based on complexity analysis
- Encapsulates decision-making

---

### 3. **Template Method Pattern** 📋

**Location**: `src/knight_journey/journey.py`

**Purpose**: Define the skeleton of the journey execution algorithm.

```python
class Journey:
    def run(self) -> Optional[Tuple[int, List[int]]]:
        for c in self.cells:
            if isinstance(c, DragonCell):
                self.strategy.on_dragon(...)
            else:
                if c.is_last:
                    ...
                else:
                    self.strategy.enforce_before_princess(...)
```

**Benefits**:
- Fixed execution flow
- Strategy-specific behavior injected at runtime
- Clear separation between algorithm and data

---

### 4. **Validator Pattern** ✅

**Location**: `src/knight_journey/cli/validator.py`

**Purpose**: Validate input data before processing.

```python
class PreflightValidator:
    @staticmethod
    def validate(cells: List[Cell], n: int) -> Optional[str]:
        # Validation logic
```

**Benefits**:
- Fail fast on invalid input
- Clear error messages
- Prevents runtime errors

---

### 5. **Facade Pattern** 🎭

**Location**: `src/knight_journey/cli/runner.py`

**Purpose**: Provide a simple interface to the complex subsystem.

```python
class JourneyRunner:
    def run(self) -> None:
        # Coordinate parser, validator, selector, journey
```

**Benefits**:
- Simple API for CLI
- Hides complexity from users
- Orchestrates multiple components

---

### 6. **Singleton Pattern** 🔐

**Location**: `src/knight_journey/logging_config.py`

**Purpose**: Ensure single logging configuration.

```python
class LogConfig:
    _configured = False
    
    @classmethod
    def setup_logging(cls, ...):
        if cls._configured:
            return
```

**Benefits**:
- Consistent logging across modules
- Prevents re-configuration
- Centralized control

---

## Project Structure

```
knight_journey_project_ci/
│
├── src/knight_journey/          # Main application package
│   ├── __init__.py              # Package initialization
│   ├── __main__.py              # Entry point
│   ├── config.py                # Configuration constants
│   ├── domain.py                # Domain models (Cell, DragonCell, PrincessCell)
│   ├── journey.py               # Journey execution engine
│   ├── strategy.py              # Strategy interface
│   ├── logging_config.py        # Logging configuration
│   │
│   ├── cli/                     # Command-line interface
│   │   ├── __init__.py
│   │   ├── parser.py            # YAML input parser
│   │   ├── runner.py            # Main CLI orchestrator (Facade)
│   │   ├── strategy_selector.py # Strategy factory
│   │   └── validator.py         # Input validator
│   │
│   └── strategies/              # Strategy implementations
│       ├── __init__.py
│       ├── heap_strategy.py     # O(n log n) heap-based strategy
│       └── buckets_strategy.py  # O(n + G) bucket-sort strategy
│
├── tests/                       # Test suite
│   ├── conftest.py             # Pytest configuration
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
│
├── docker/                     # Docker documentation
│   └── README_DOCKER.md
│
├── .github/                    # GitHub Actions CI/CD
│   ├── workflows/
│   │   ├── ci.yml             # Continuous Integration
│   │   └── release.yml        # Release automation
│   └── PULL_REQUEST_TEMPLATE.md
│
├── Dockerfile                  # Multi-stage Docker build
├── docker-compose.yml          # Docker Compose configuration
├── .dockerignore              # Docker build exclusions
├── Makefile                   # Development automation
├── pyproject.toml             # Project metadata & dependencies
├── input.yaml                 # Example input file
└── README.md                  # User documentation
```

---

## Core Components

### Domain Layer (`domain.py`)

**Immutable domain models using dataclasses:**

```python
@dataclass(frozen=True)
class Cell(ABC):
    idx: int

@dataclass(frozen=True)
class DragonCell(Cell):
    gold: int

@dataclass(frozen=True)
class PrincessCell(Cell):
    beauty: int
    is_last: bool = False
```

**Design decisions**:
- Frozen dataclasses for immutability
- ABC for type safety
- Simple, focused models

---

### Strategy Layer (`strategies/`)

#### HeapStrategy - O(n log n)

**Algorithm**:
1. Add all dragons to min-heap
2. At each princess, pop cheapest dragons until constraint satisfied
3. Track selections with boolean array

**Best for**: Large gold values (G >> n log n)

**Space**: O(n)
**Time**: O(n log n)

#### BucketsStrategy - O(n + G)

**Algorithm**:
1. Create buckets for each gold value [0..G]
2. Track minimum non-empty bucket
3. Remove from cheapest bucket in O(1)

**Best for**: Small gold values (G < n log n)

**Space**: O(G + n)
**Time**: O(n + G)

---

### CLI Layer (`cli/`)

#### InputParser
- Reads YAML files
- Converts to domain objects
- Tracks max gold value

#### PreflightValidator
- Validates constraints
- Returns descriptive errors
- Prevents runtime failures

#### StrategySelector (Factory)
- Analyzes complexity
- Selects optimal strategy
- Configurable threshold

#### JourneyRunner (Facade)
- Orchestrates workflow
- Handles errors gracefully
- Formats output

---

## Data Flow

```
┌─────────────┐
│ input.yaml  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  InputParser    │  Reads & parses YAML
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│PreflightValidator│ Validates constraints
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│StrategySelector │ Chooses algorithm
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│    Journey      │ Executes algorithm
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│     Output      │ Prints results
└─────────────────┘
```

---

## Algorithm Selection

### Complexity Analysis

```python
heap_complexity = n * log(n)
buckets_complexity = n + max_gold

if heap_complexity < buckets_complexity * 0.9:
    use HeapStrategy
else:
    use BucketsStrategy
```

### Decision Matrix

| n | max_gold | Selected Strategy | Reason |
|---|----------|------------------|--------|
| 1000 | 10 | Heap | G very small |
| 1000 | 100 | Heap | n log n < n + G |
| 1000 | 10000 | Heap | Similar complexity |
| 1000 | 1000000 | Buckets | G >> n log n |

---

## Extension Points

### Adding New Strategies

1. Create new class in `strategies/`:

```python
class MyStrategy(KillingStrategy):
    def on_dragon(self, gold: int, pos: int) -> None:
        # Implementation
    
    def enforce_before_princess(self, beauty: int) -> None:
        # Implementation
    
    # ... other methods
```

2. Update `StrategySelector`:

```python
def choose(self) -> KillingStrategy:
    if condition:
        return MyStrategy(...)
```

3. Add tests in `tests/unit/test_strategy/`

---

### Adding New Cell Types

1. Add domain model in `domain.py`:

```python
@dataclass(frozen=True)
class TreasureCell(Cell):
    gems: int
```

2. Update parser to recognize new type
3. Update journey logic
4. Update validator

---

### Adding New Input Formats

1. Create new parser class:

```python
class JSONParser:
    def parse(self) -> Tuple[List[Cell], int, int]:
        # Implementation
```

2. Update runner to detect format
3. Add tests

---

## Configuration Management

All configuration centralized in `config.py`:

```python
class ValidationConfig:
    MAX_GOLD = 10_000_000
    MAX_BEAUTY = 200_000

class StrategyConfig:
    HEAP_THRESHOLD_MULTIPLIER = 0.9
```

**Benefits**:
- Single source of truth
- Easy to modify
- Type-safe constants

---

## Error Handling Strategy

### Layers of Protection

1. **Input Validation** - Catch errors early
2. **Type System** - Prevent type errors
3. **Exception Handling** - Graceful degradation
4. **Logging** - Observable errors

### Error Flow

```
Input Error → PreflightValidator → Return error message
Parse Error → InputParser → Caught by runner → Print -1
Runtime Error → Journey → Caught by runner → Print -1
```

---

## Testing Architecture

### Test Organization

```
tests/
├── unit/           # Isolated component tests
│   ├── test_domain/
│   ├── test_strategy/
│   ├── test_parser/
│   └── test_validator/
└── integration/    # End-to-end tests
    ├── test_cli_success.py
    └── test_cli_failure.py
```

### Test Principles

- **Isolation** - Each test is independent
- **Coverage** - Aim for >90%
- **Speed** - Fast unit tests
- **Clarity** - Descriptive test names

---

## Performance Considerations

### Time Complexity

| Component | Complexity | Notes |
|-----------|-----------|-------|
| Parsing | O(n) | Linear file read |
| Validation | O(n) | Single pass |
| HeapStrategy | O(n log n) | Heap operations |
| BucketsStrategy | O(n + G) | Bucket initialization |
| Output | O(k) | k = killed dragons |

### Space Complexity

| Component | Complexity | Notes |
|-----------|-----------|-------|
| Domain Objects | O(n) | Cell list |
| HeapStrategy | O(n) | Heap + selection array |
| BucketsStrategy | O(G + n) | Buckets + selection |

---

## Security Considerations

1. **Input Validation** - Prevent malicious input
2. **Resource Limits** - Max gold, beauty values
3. **Non-root Docker** - Security best practice
4. **Dependency Scanning** - CI/CD pipeline
5. **No eval/exec** - Safe parsing only

---

## Future Enhancements

### Possible Improvements

1. **Parallel Processing** - Process multiple inputs concurrently
2. **Caching** - Memoize repeated calculations
3. **Streaming** - Handle very large inputs
4. **API Server** - REST/GraphQL interface
5. **Database** - Store results persistently
6. **Visualization** - Web UI for results
7. **Optimization** - Profile and optimize hotspots

---

## References

- [Strategy Pattern](https://refactoring.guru/design-patterns/strategy)
- [Factory Pattern](https://refactoring.guru/design-patterns/factory-method)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

