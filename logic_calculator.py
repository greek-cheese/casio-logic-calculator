import logic_operators, syntax_tree, tokenizer

def tokenize_expression(expression):
    """
    Tokenizes a logical expression into a list of tokens.

    Args:
        expression (str): The propositional logic expression to tokenize.

    Returns:
        List[Token]: A list of tokens representing the input expression, where each token is an operand,
                     operator, or parenthesis.

    Raises:
        ValueError: If an unknown character is encountered in the expression.
    """
    tokens = []
    expression = expression.upper()
    index = 0
    while index < len(expression):
        char = expression[index]
        if char.isspace():
            index += 1
            continue
        if char == "(":
            tokens.append(tokenizer.Token(tokenizer.TokenType.PARENTHESIS, "("))
            index += 1
            continue
        elif char == ")":
            tokens.append(tokenizer.Token(tokenizer.TokenType.PARENTHESIS, ")"))
            index += 1
            continue
        if expression[index:index+4] == "TRUE":
            tokens.append(tokenizer.Token(tokenizer.TokenType.OPERAND, True))
            index += 4
            continue
        elif expression[index:index+5] == "FALSE":
            tokens.append(tokenizer.Token(tokenizer.TokenType.OPERAND, False))
            index += 5
            continue
        for op in logic_operators.operators.keys():
            if expression[index:index+len(op)] == op:
                precedence, func = logic_operators.operators[op]
                associativity = "right" if op == "NOT" else "left"
                tokens.append(tokenizer.Token(tokenizer.TokenType.OPERATOR,op,precedence,associativity,func))
                index += len(op)
                break
        else:
            if len(char) == 1 and char.isalpha():
                tokens.append(tokenizer.Token(tokenizer.TokenType.OPERAND, char))
                index += 1
            else:
                raise ValueError("Unknown character: " + str(char))
    return tokens

def build_ast(tokens):
    """
    Builds an Abstract Syntax Tree (AST) from a list of tokens representing a logical expression.

    Args:
        tokens (List[Token]): A list of tokens representing a logical expression.

    Returns:
        ASTNode: The root node of the AST.

    Raises:
        ValueError: If an unexpected token is encountered during parsing.
    """
    def parse_primary():
        token = tokens.pop(0)
        if token.token_type == tokenizer.TokenType.OPERAND:
            return syntax_tree.ASTNode(token.value)
        elif token.token_type == tokenizer.TokenType.PARENTHESIS and token.value == "(":
            node = build_ast(tokens)  # Parse sub-expression
            if tokens and tokens[0].value == ")":  # Make sure we have the closing parenthesis
                tokens.pop(0)  # Remove closing ')'
            return node
        elif token.token_type == tokenizer.TokenType.OPERATOR and token.value == "NOT":
            operand = parse_primary()  # NOT is unary, so only one operand
            return syntax_tree.ASTNode(token.value, left=operand)
        else:
            raise ValueError("Unexpected token: " + str(token))
    def parse_operator(precedence_level):
        node = parse_primary()
        while tokens and tokens[0].token_type == tokenizer.TokenType.OPERATOR and tokens[0].precedence >= precedence_level:
            token = tokens.pop(0)
            next_precedence = token.precedence + 1 if token.associativity == "left" else token.precedence
            right = parse_operator(next_precedence)
            node = syntax_tree.ASTNode(token.value, left=node, right=right)
        return node
    return parse_operator(0)

def evaluate_tree(node, variable_values=None):
    """
    Evaluates an Abstract Syntax Tree (AST) for a logical expression.

    Args:
        node (ASTNode): The root node of the AST to evaluate.
        variable_values (dict, optional): A dictionary mapping variable names to their boolean values. 
                                          If not provided, all variables default to False.

    Returns:
        bool: The result of the logical expression evaluation.

    Raises:
        ValueError: If an operator's associated function cannot be found.
    """
    if variable_values is None:
        variable_values = {}
    if node.left is None and node.right is None:
        if isinstance(node.value, str):  # Variable (like P, Q, etc.)
            return variable_values.get(node.value, False)  # Default to False if not found
        else:
            return node.value  # Constant value (True or False)
    if node.left is not None and node.right is None:
        operand = evaluate_tree(node.left, variable_values)
        return logic_operators.operators[node.value][1](operand)
    left_value = evaluate_tree(node.left, variable_values)
    right_value = evaluate_tree(node.right, variable_values)
    return logic_operators.operators[node.value][1](left_value, right_value)

def generate_truth_combinations(n):
    """
    Generates all possible combinations of truth values for n variables.

    Args:
        n (int): The number of variables.

    Returns:
        List[List[int]]: A list of combinations, where each combination is a list of 0s and 1s
                         representing truth values (False and True).
    """
    truth_values = []
    for i in range(2 ** n):  # There are 2^n combinations for n variables
        combination = []
        for j in range(n):
            combination.append((i >> j) & 1)  # Extract the j-th bit from i (0 or 1)
        truth_values.append(combination[::-1])  # Reverse to match the correct order
    return truth_values

def generate_truth_table(ast, variables, return_as_dict=False, print_table=True):
    """
    Generates and optionally prints the truth table for a given logical expression.

    Args:
        ast (ASTNode): The root node of the AST representing the logical expression.
        variables (List[str]): A list of variable names used in the expression.
        return_as_dict (bool, optional): Whether to return the table as a list of dictionaries where
                                         each row is a dictionary. Default is False.
        print_table (bool, optional): Whether to print the table. Default is True.

    Returns:
        List[List[int]] or List[dict]: The truth table for the expression. Each row is either a list of
                                       truth values or a dictionary depending on `return_as_dict`.
    """
    combinations = generate_truth_combinations(len(variables))
    table = []
    if print_table:
        print(' | '.join(variables) + " | RESULT")
        print('-' * (4 * len(variables) + 9))
    for combination in combinations:
        variable_values = {var: bool(val) for var, val in zip(variables, combination)}
        result = evaluate_tree(ast, variable_values)
        result_val = 1 if result else 0
        if return_as_dict:
            row = {var: val for var, val in zip(variables, combination)}
            row['RESULT'] = result_val
        else:
            row = list(combination) + [result_val]
        table.append(row)
        if print_table:
            combination_str = ' | '.join(map(str, combination))
            print(combination_str + " | " + str(result_val))
    return table

def extract_logical_variables(node, variables=None):
    """
    Extracts all logical variables (operands) from an Abstract Syntax Tree (AST).

    Args:
        node (ASTNode): The root node of the AST.
        variables (set, optional): A set to store extracted variables. Default is None.

    Returns:
        set: A set of variable names (str) used in the logical expression.
    """
    if variables is None:
        variables = set()
    if node.left is None and node.right is None:
        if isinstance(node.value, str):  # It's a variable
            variables.add(node.value)
    if node.left:
        extract_logical_variables(node.left, variables)
    if node.right:
        extract_logical_variables(node.right, variables)
    return variables

def main():
    """
    The main loop that interacts with the user, taking logical expressions as input, tokenizing them,
    building an AST, and evaluating or generating a truth table for the expression.

    Prompts the user for an expression, tokenizes it, parses it into an AST, and prints the result or
    truth table. Special commands like 'Q', 'X', 'QUIT', or 'EXIT' terminate the loop, and 'H' or 'HELP'
    prints available operators.

    Raises:
        Exception: Any errors during tokenization, parsing, or evaluation are caught and displayed to the user.
    """
    while True:
        expression = input("Prop Exp? ").strip().upper()
        if expression in ["Q", "X", "QUIT", "EXIT"]:
            break
        if expression in ["H", "HELP"]:
            print("NOT; AND; OR; XOR; IMP; IFF;")
            continue
        try:
            tokens = tokenize_expression(expression)
            ast = build_ast(tokens)
            variables = sorted(extract_logical_variables(ast))
            if variables:
                generate_truth_table(ast, variables)
            else:
                result = evaluate_tree(ast)
                print("Result: " + result)
        except Exception as e:
            print("Err: " + str(e))

main()