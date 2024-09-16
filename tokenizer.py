# TokenType defines the possible types of tokens in the logical expression
class TokenType:
    OPERATOR = "OPERATOR"
    OPERAND = "OPERAND"
    PARENTHESIS = "PARENTHESIS"


class Token:
    def __init__(self, token_type, value, precedence=None, associativity=None, func=None):
        """
        Args:
            token_type (str): The type of the token (operator, operand, parenthesis).
            value (str or bool): The value of the token.
            precedence (int, optional): Operator precedence (only applicable for operators).
            associativity (str, optional): Operator associativity ('left' or 'right').
            func (callable, optional): The function for evaluating the operator.
        """
        self.token_type = token_type
        self.value = value
        self.precedence = precedence
        self.associativity = associativity
        self.func = func

    def __repr__(self):
        return "Token(type="+str(self.token_type)+", value="+str(self.value)+", precedence="+str(self.precedence)+")"