# micro nodes
# by las-r

# data nodes
class LiteralNode:
    def __init__(self, value):
        self.value = value
    
    def eval(self, env):
        return self.value
    
# operation nodes
class UnaryOpNode:
    def __init__(self, op, a):
        self.op = op
        self.a = a
    
    def eval(self, env):
        a = self.a.eval(env)
        if self.op == "-": return -a
        if self.op == "~": return ~a
        if self.op == "!": return int(not a)
        raise Exception(f"Unknown unary operator: {self.op}")
    
class BinaryOpNode:
    def __init__(self, a, op, b):
        self.a = a
        self.op = op
        self.b = b
    
    def eval(self, env):
        a = self.a.eval(env)
        b = self.b.eval(env)
        if self.op == "+": return a + b
        if self.op == "-": return a - b
        if self.op == "*": return a * b
        if self.op == "/": return a / b
        if self.op == "&": return a & b
        if self.op == "|": return a | b
        if self.op == "^": return a ^ b
        if self.op == "==": return int(a == b)
        if self.op == "<=": return int(a <= b)
        if self.op == ">=": return int(a >= b)
        if self.op == "<": return int(a < b)
        if self.op == ">": return int(a > b)
        if self.op == "&&": return int(a and b)
        if self.op == "||": return int(a or b)
        raise Exception(f"Unknown binary operator: {self.op}")