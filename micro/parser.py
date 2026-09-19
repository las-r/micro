from .nodes import *

# micro parser
# by las-r

# operator lists
UNOPS = ["-", "~", "!"]
BINOPS = ["+", "-", "*", "/", "&", "|", "^", "==", "<=", ">=", "<", ">", "&&", "||"]

# atom parser
def parseatom(tokens):
    # unary ops
    if tokens.peek() in UNOPS:
        op = tokens.eat()
        a = parseatom(tokens)
        return UnaryOpNode(op, a)
    
    # parentheses
    if tokens.peek() == "(":
        tokens.eat()
        expr = parseexpr(tokens)
        tokens.eat()
        return expr
    
    # literal
    tok = tokens.eat()
    if tok.startswith('"') and tok.endswith('"'):
        return LiteralNode(tok[1:-1])
    try:
        return LiteralNode(int(tok))
    except ValueError:
        return LiteralNode(float(tok))

# expression parser
def parseexpr(tokens):
    a = parseatom(tokens)
    while tokens.can_eat() and tokens.peek() in BINOPS:
        op = tokens.eat()
        b = parseatom(tokens)
        a = BinaryOpNode(a, op, b)
    return a