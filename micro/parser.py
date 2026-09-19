from .nodes import *

# micro parser
# by las-r

# operators
BINARYOP = ["+", "-", "*", "/", "&", "|", "^", "==", "<", "<=", ">", ">=", "&&", "||"]
UNARYOP = ["-", "~", "!"]

# parser function
def parse():
    pass

# expression parser
def exprparse(tokens):
    a = atomparse(tokens)
    while tokens.peek() is not None and tokens.peek() != ")":
        op = tokens.next()
        b = atomparse(tokens)
        a = BinaryOpNode(a, op, b)
    return a

# atom parser
def atomparse(tokens):
    token = tokens.next()
    
    # unary ops
    if token in UNARYOP:
        node = atomparse(tokens)
        return UnaryOpNode(token, node)

    # parentheses
    if token == '(':
        node = exprparse(tokens)
        closing = tokens.next()
        if closing != ')':
            raise SyntaxError("Expected matching ')'")
        return node

    # strings
    if len(token) >= 2 and token[0] == token[-1] == '"':
        val = token[1:-1]
        return LiteralNode(val)

    # numbers and variables
    try:
        val = float(token)
        return LiteralNode(int(val) if val.is_integer() else val)
    except ValueError:
        return VariableNode(token)