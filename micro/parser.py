import re
from micro.nodes import *

# micro parser
# by las-r

# constant lists
UNOPS = ["-", "~", "!"]
BINOPS = ["+", "-", "*", "/", "%", "&", "|", "^", "==", "<=", ">=", "<", ">", "&&", "||"]
ESCAPES = {"n": "\n", "t": "\t", "r": "\r"}

# atom parser
def parseatom(tokens, index=True):
    # array literals
    if tokens.peek() == "[":
        tokens.eat()
        items = []
        if tokens.peek() != "]":
            items.append(parseexpr(tokens))
            while tokens.peek() == ",":
                tokens.eat()
                items.append(parseexpr(tokens))
        tokens.expect_value("]")
        node = ArrayNode(items)
        while index and tokens.peek() == ":":
            tokens.eat()
            iexpr = parseatom(tokens, False)
            node = IndexNode(node, iexpr)
        return node

    # unary ops
    if tokens.peek() in UNOPS:
        op = tokens.eat()
        a = parseatom(tokens, index)
        return UnaryOpNode(op, a)

    # parentheses
    if tokens.peek() == "(":
        tokens.eat()
        expr = parseexpr(tokens)
        tokens.expect_value(")")
        node = expr
        while index and tokens.peek() == ":":
            tokens.eat()
            iexpr = parseatom(tokens, False)
            node = IndexNode(node, iexpr)
        return node

    # literal, variable, and function call
    tok = tokens.eat()
    c = tok[0]
    if c == '"':
        node = LiteralNode(re.sub(r"\\(.)", lambda m: ESCAPES.get(m.group(1), m.group(1)), tok[1:-1]))
    elif c.isdigit():
        node = LiteralNode(float(tok) if "." in tok else int(tok))
    elif c.isalpha() or c == "_":
        if tokens.peek() == "(":
            tokens.eat()
            args = []
            if tokens.peek() != ")":
                args.append(parseexpr(tokens))
                while tokens.peek() == ",":
                    tokens.eat()
                    args.append(parseexpr(tokens))
            tokens.expect_value(")")
            node = CallNode(tok, args)
        else:
            node = VariableNode(tok)
    else:
        raise SyntaxError(f"Unexpected token: {tok}")

    # array indexing
    while index and tokens.peek() == ":":
        tokens.eat()
        iexpr = parseatom(tokens, False)
        node = IndexNode(node, iexpr)

    return node

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
    # if statement
    if tokens.peek() == "if":
        tokens.eat()
        cond = parseexpr(tokens)
        body = []
        while tokens.can_eat() and tokens.peek() not in ("else", "end"):
            body.append(parsestmt(tokens))
        ebody = []
        if tokens.peek() == "else":
            tokens.eat()
            while tokens.can_eat() and tokens.peek() != "end":
                ebody.append(parsestmt(tokens))
        tokens.expect_value("end")
        return IfNode(cond, body, ebody)
    
    # while statement
    if tokens.peek() == "while":
        tokens.eat()
        cond = parseexpr(tokens)
        body = []
        while tokens.can_eat() and tokens.peek() != "end":
            body.append(parsestmt(tokens))
        tokens.expect_value("end")
        return WhileNode(cond, body)
    
    # break statement
    if tokens.peek() == "break":
        tokens.eat()
        return BreakNode()
    
    # function definition statement
    if tokens.peek() == "func":
        tokens.eat()
        name = tokens.eat()
        params = []
        if tokens.peek() == "(":
            tokens.eat()
            if tokens.peek() != ")":
                params.append(tokens.eat())
                while tokens.peek() == ",":
                    tokens.eat()
                    params.append(tokens.eat())
            tokens.expect_value(")")
        body = []
        while tokens.can_eat() and tokens.peek() != "end":
            body.append(parsestmt(tokens))
        tokens.expect_value("end")
        return FunctionNode(name, params, body)
    
    # return statement
    if tokens.peek() == "return":
        tokens.eat()
        if tokens.can_eat() and tokens.peek() not in ["end", "if", "else", "while", "func"]:
            expr = parseexpr(tokens)
        else:
            expr = None
        return ReturnNode(expr)
    
    # import statement
    if tokens.peek() == "import":
        tokens.eat()
        path = parseexpr(tokens)
        return ImportNode(path)
    
    # assignment
    lhs = parseexpr(tokens)
    if tokens.peek() == "=":
        tokens.eat()
        rhs = parseexpr(tokens)
        if isinstance(lhs, VariableNode):
            return AssignNode(lhs.name, rhs)
        if isinstance(lhs, IndexNode):
            return IndexAssignNode(lhs.arr, lhs.idx, rhs)
        raise SyntaxError("Invalid assignment target")
    
    # fallback expression
    return lhs

# parser
def parse(tokens):
    nodes = []
    while tokens.can_eat():
        nodes.append(parsestmt(tokens))
    return nodes