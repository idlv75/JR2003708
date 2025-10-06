# DOCS for "Dragons and Princesses" codeforces solution
## Introduction
This is my (Eyal Levi), proposed solution for the Dragons and princesses code problem.

## Project Structure
- `main.py` - the solution, comprised of a `main` function, a `solve` function which has most of the logic, and a helper function called `printer`
- `reader.py` - where the yaml reading and parsing functions will reside. I will use a factory in the parser so that if need be, more types could be added. 
- `factory.py` - where the princess and dragon types will reside. In addition I've added a type factory which parses the input, so that newer types could be more easily added down the road.
- `test.py` - the unit tests 
- `input.yaml` - a general example input file
- `docs.md` - this very file, which gives further information about the project and the implementation

## Format For YAML input file
```yaml
name-of-game:
    - number_of_cells: <cell-number>
    - game:
      - p 2
      - d 1
      - d 3
      - p 1
```

## Tests
Tests are located in test.py, using python's built in unittest module.
