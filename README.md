# Gem Hunter Solvers

## Description:
This project implements multiple solvers for the Gem Hunter (originally from the game Minesweeper) game.

## Install Libraries:
The project requires the following libraries to be installed: PySAT, Tabulate.
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
The output will be the solved grid, saved in a file named `output.txt` in the same directory.\
If the grid is unsolvable, the output will be an empty file.\
The results will also be printed in the console.\
The CNFs generated for the grid will be saved in a file named `CNFs.txt` in the same directory of the test case.

## Benchmark:
The `benchmark.py` script can be used to run all algorithms on all test cases and measure the time taken to solve each grid.\
The results will be saved in a file named `benchmark.txt` in the same directory.
To run the benchmark, use the following command:
```bash
python benchmark.py
```

## Example of benchmark output:
```bash
| Test case   | CNFs   | Empty cells   | Traps   | Algorithm    | Time        | Model hash (binary)                                 |
|-------------+--------+---------------+---------+--------------+-------------+-----------------------------------------------------|
| 5x5         | 27     | 8             | 4       | pysat        | 0.2227 ms   | 156                                                 |
| 5x5         | 27     | 8             | 4       | dpll         | 0.0805 ms   | 156                                                 |
| 5x5         | 27     | 8             | 4       | backtracking | 0.0864 ms   | 156                                                 |
| 5x5         | 27     | 8             | 4       | bruteforce   | 0.3599 ms   | 156                                                 |
| -           | -      | -             | -       | -            | -           | -                                                   |
| 9x9         | 153    | 32            | 20      | pysat        | 0.6009 ms   | 3219758312                                          |
| 9x9         | 153    | 32            | 20      | dpll         | 0.9405 ms   | 3219758312                                          |
| 9x9         | 153    | 32            | 20      | backtracking | 1.9873 ms   | 3219758312                                          |
| 9x9         | 153    | 32            | 20      | bruteforce   | N/A         | 3219758312                                          |
| -           | -      | -             | -       | -            | -           | -                                                   |
| 11x11       | 232    | 41            | 25      | pysat        | 0.8373 ms   | 2190420907660                                       |
| 11x11       | 232    | 41            | 25      | dpll         | 2.0941 ms   | 2190420907660                                       |
| 11x11       | 232    | 41            | 25      | backtracking | 4.0226 ms   | 2190420907660                                       |
| 11x11       | 232    | 41            | 25      | bruteforce   | N/A         | 2190420907660                                       |
| -           | -      | -             | -       | -            | -           | -                                                   |
| 15x15       | 493    | 94            | 30      | pysat        | 1.6619 ms   | 1287437542759197841967678982                        |
| 15x15       | 493    | 94            | 30      | dpll         | 8.7558 ms   | 1287437542759197841967678982                        |
| 15x15       | 493    | 94            | 30      | backtracking | 14.2824 ms  | 1287437542759197841967678982                        |
| 15x15       | 493    | 94            | 30      | bruteforce   | N/A         | 1287437542759197841967678982                        |
| -           | -      | -             | -       | -            | -           | -                                                   |
| 20x20       | 822    | 170           | 50      | pysat        | 2.6279 ms   | 406298892182285317047186185263105794068306773178241 |
| 20x20       | 822    | 170           | 50      | dpll         | 23.8342 ms  | 406298892182285317047186185263105794068306773178241 |
| 20x20       | 822    | 170           | 50      | backtracking | 838.7302 ms | 406298892182285317047186185263105794068306773178241 |
| 20x20       | 822    | 170           | 50      | bruteforce   | N/A         | 406298892182285317047186185263105794068306773178241 |
```


