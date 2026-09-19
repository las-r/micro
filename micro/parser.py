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
    
    # literal and variable
    tok = tokens.eat()
    if tok.startswith('"') and tok.endswith('"'):
        return LiteralNode(tok[1:-1])
    try:
        return LiteralNode(int(tok))
    except ValueError:
        try:
            return LiteralNode(float(tok))
        except ValueError:
            return VariableNode(tok)

# expression parser
def parseexpr(tokens):
    a = parseatom(tokens)
    while tokens.can_eat() and tokens.peek() in BINOPS:
        op = tokens.eat()
        b = parseatom(tokens)
        a = BinaryOpNode(a, op, b)
    return a

# statement parser
def parsestmt(tokens):
    # temporary output statement
    if tokens.peek() == "out":
        tokens.eat()
        expr = parseexpr(tokens)
        return OutputNode(expr)
    
    # if statement
    if tokens.peek() == "if":
        tokens.eat()
        cond = parseexpr(tokens)
        body = []
        while tokens.can_eat() and tokens.peek() not in ("else", "end"):
            body.append(parsestmt(tokens))
        ebody = []
        if tokens.peek() == "else":
            while tokens.can_eat() and tokens.peek() != "end":
                ebody.append(parsestmt(tokens))
        if tokens.peek() == "end":
            tokens.eat()
        return IfNode(cond, body, ebody)
    
    # while statement
    if tokens.peek() == "while":
        tokens.eat()
        cond = parseexpr(tokens)
        body = []
        while tokens.can_eat() and tokens.peek() != "end":
            body.append(parsestmt(tokens))
        if tokens.peek() == "end":
            tokens.eat()
        return WhileNode(cond, body)
    
    # break statement
    if tokens.peek() == "break":
        tokens.eat()
        return BreakNode()
    
    # variable assignment
    if tokens.can_eat() and tokens.peek(1) == "=":
        name = tokens.eat()
        tokens.eat()
        expr = parseexpr(tokens)
        return AssignNode(name, expr)

    # fallback expression parse
    return parseexpr(tokens)

# parser
def parse(tokens):
    nodes = []
    while tokens.can_eat():
        nodes.append(parsestmt(tokens))
    return nodes