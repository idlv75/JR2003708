# Dragons and Princesses Solution

Python solution for CodeForces Problem #548.

## Solution Requirements
- ✅ Implemented in Python
- ✅ Python script is executable 
- ✅ Input consumed as YAML file with example provided
- ✅ Submitted as Pull Request to this repository

## How to stand out from the crowd
- ✅ **Code Style**: Clean, well-documented code with type hints
- ✅ **Immutability**: Uses dataclasses for immutable data structures
- ✅ **Unittests**: Comprehensive test coverage

## Features
- Greedy algorithm with Union-Find data structure
- YAML input support
- Unit tests
- Docker support
- CI pipeline

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run with YAML input
python dragons_and_princesses.py input.yaml

# Run with standard input
python dragons_and_princesses.py < input.txt

# Run tests
python test_dragons_and_princesses.py

# Docker
docker build -t dragons-princesses .
docker run --rm dragons-princesses python dragons_and_princesses.py input.yaml
```

## Input Format

YAML:
```yaml
n: 5
cells:
  - type: "d"
    value: 10
    position: 2
  - type: "p"
    value: 2
    position: 3
```

Standard:
```
5
d 10
p 2
```

## Output
```
10
1
2
```

## Author
Amit Barda - amit11barda@gmail.com
