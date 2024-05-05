# Gem Hunter Solver

## Description:
This project is a solver for the Gem Hunter (originally from the game Minesweeper) game.

## Required Libraries:
```bash
pip install -r requirements.txt
```

## Usage:
```bash
python main.py <algorithm> <test_case>
```

## Arguments:
- algorithm: The algorithm to be used to solve the game. The available algorithms are:
  - `pysat`: Uses the PySAT library to solve the game.
  - `dpll`: Uses the DPLL algorithm to solve the game.
  - `backtracking`: Uses backtracking to solve the game.
  - `bruteforce`: Uses brute force to solve the game.
- test_case: The test case to be solved. The available test cases are:
  - `5x5`: A 5x5 grid.
  - `9x9`: A 9x9 grid.
  - `11x11`: A 11x11 grid.
  - `15x15`: A 15x15 grid.
  - `20x20`: A 20x20 grid.

## Example:
```bash
python main.py pysat 5x5
```

## Output:
After reading input from the file `testcases/5x5/input.txt`, the program will solve the grid using the PySAT algorithm.\
The output will be the solved grid, saved in a file named `output.txt` in the same directory.



