# ASTNode represents a node in the Abstract Syntax Tree (AST) for logical expressions
class ASTNode:
    def __init__(self, value, left=None, right=None):
        """
        Args:
            value (str or bool): The value of the node, which can be an operator, operand, or result.
            left (ASTNode, optional): The left child node in the AST (default is None).
            right (ASTNode, optional): The right child node in the AST (default is None).
        """
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        """
        Returns a string representation of the ASTNode.
        If the node has both left and right children, it returns (left value right).
        If the node only has a left child, it returns (value left).
        Otherwise, it returns the value itself.
        """
        if self.left and self.right:
            return "(" + str(self.left) + " " + str(self.value) + " " + str(self.right) + ")"
        elif self.left:
            return "(" + str(self.value) + " " + str(self.left) + ")"
        else:
            return str(self.value)