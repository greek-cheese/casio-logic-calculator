# Logical operators with their precedence and evaluation functions
# Format: "OPERATOR": [precedence, lambda function]

operators = {
    "NOT": [1, lambda a: int(not a)], # Unary NOT
    "AND": [2, lambda a, b: int(a and b)], # Binary AND
    "XOR": [3, lambda a, b: int(a != b)],  # Binary XOR (exclusive OR)
    "OR":  [4, lambda a, b: int(a or b)],  # Binary OR
    "IMP": [5, lambda a, b: int(not a or b)], # Implication (if a then b)
    "IFF": [6, lambda a, b: int(a == b)]   # If and only if (logical equivalence)
}