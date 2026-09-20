from .nodes import *

# micro parser
# by las-r

# operator lists
UNOPS = ["-", "~", "!"]
BINOPS = ["+", "-", "*", "/", "%", "&", "|", "^", "==", "<=", ">=", "<", ">", "&&", "||"]

# atom parser
def parseatom(tokens):
    # array literals
    if tokens.peek() == "[":
        tokens.eat()
        items = []
        if tokens.peek() != "]":
            items.append(parseexpr(tokens))
            while tokens.peek() == ",":
                tokens.eat()
                items.append(parseexpr(tokens))
        if tokens.peek() == "]":
            tokens.eat()
        else:
            raise SyntaxError(f"Expected closing ']' in array definition")
        node = ArrayNode(items)
        while tokens.peek() == ":":
            tokens.eat()
            iexpr = parseatom(tokens)
            node = IndexNode(node, iexpr)
        return node

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
        node = expr
        while tokens.peek() == ":":
            tokens.eat()
            iexpr = parseatom(tokens)
            node = IndexNode(node, iexpr)
        return node

    # literal, variable, and function call
    tok = tokens.eat()
    if tok.startswith('"') and tok.endswith('"'):
        node = LiteralNode(tok[1:-1])
    else:
        try:
            node = LiteralNode(int(tok))
        except ValueError:
            try:
                node = LiteralNode(float(tok))
            except ValueError:
                if tokens.peek() == "(":
                    tokens.eat()
                    args = []
                    if tokens.peek() != ")":
                        args.append(parseexpr(tokens))
                        while tokens.peek() == ",":
                            tokens.eat()
                            args.append(parseexpr(tokens))
                    if tokens.peek() == ")":
                        tokens.eat()
                    else:
                        raise SyntaxError(f"Expected closing ')' in function call '{tok}'")
                    node = CallNode(tok, args)
                else:
                    node = VariableNode(tok)

    # array indexing
    while tokens.peek() == ":":
        tokens.eat()
        iexpr = parseatom(tokens)
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
            if tokens.peek() == ")":
                tokens.eat()
            else:
                raise SyntaxError(f"Expected closing ')' in definition of '{name}'")
        body = []
        while tokens.can_eat() and tokens.peek() != "end":
            body.append(parsestmt(tokens))
        if tokens.peek() == "end":
            tokens.eat()
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