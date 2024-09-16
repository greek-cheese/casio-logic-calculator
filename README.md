# casio-logic-calculator
Propositional logic calculator/table generator for Python and Casio fx-9750GIII MicroPython.

It supports several common logical operators and is capable of parsing and evaluating expressions with variables and parentheses. Additionally, it was specifically designed to run on the Casio fx-9750GIII graphic calculator using MicroPython.

## Features

- **Supported Operators**:
    - `NOT` (negation)
    - `AND` (conjunction)
    - `OR` (disjunction)
    - `XOR` (exclusive OR)
    - `IMP` (implication)
    - `IFF` (biconditional)
    - Additional operators can be easily added in the `logic_operators.py` file.

- **Evaluate Expressions**: Provide logical expressions for evaluation, with variables automatically handled.
- **Generate Truth Tables**: Automatically generate and print truth tables for expressions.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/greek-cheese/casio-logic-calculator.git
    cd casio-logic-calculator
    ```

2. Run the calculator:
    ```bash
    python3 logic_calculator.py
    ```

For **Casio fx-9750GIII MicroPython**:
1. Due to Casio's strict requirements, it is necessary to remove all docstrings and comments from the methods to fit within the 150 lines per file and 127 characters per line limits.

2. Connect the calculator to the PC, and copy all the `.py` files to the main memory in the dedicated folder. You can copy the whole repo, but to save memory, only the `.py` files are required for the calculator to run.

3. Turn on the calculator → `MENU` → `H` (Python App) → (project_folder) + `F2` (Open) → `logic_calculator.py` + `F1` (Run).

## Usage

Once the calculator is running, you can enter a propositional logic expression to generate its truth table or evaluate it. The calculator supports single-character alphabetic variables, logical operators, and `TRUE`/`FALSE` values. To get help or exit the program, use `H` and `Q`, respectively. The calculator automatically uppercases the expression, so you don't need to worry about using the shift button.

### Example:
```python
>>> Prop Exp? P AND (Q OR NOT P)
P | Q | RESULT
-----------------
0 | 0 | 0
0 | 1 | 0
1 | 0 | 0
1 | 1 | 1
```

### Special Commands

- Enter `Q`, `X`, `QUIT`, or `EXIT` to exit the program.
- Enter `H` or `HELP` to display the list of available operators.
