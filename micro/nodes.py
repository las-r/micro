# micro nodes
# by las-r

# temporary output node
class OutputNode:
    def __init__(self, expr):
        self.expr = expr
    
    def eval(self, env):
        print(self.expr.eval(env))

# literal node
class LiteralNode:
    def __init__(self, value):
        self.value = value
    
    def eval(self, env):
        return self.value

# variable nodes
class VariableNode:
    def __init__(self, name):
        self.name = name
    
    def eval(self, env):
        if self.name in env:
            return env[self.name]
        raise Exception(f"Undefined variable: {self.name}")

class AssignNode:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr
    
    def eval(self, env):
        env[self.name] = self.expr.eval(env)
    
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
        if self.op == "&&": return int(a and self.b.eval(env))
        if self.op == "||": return int(a or self.b.eval(env))
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
        raise Exception(f"Unknown binary operator: {self.op}")
    
# control flow nodes
class IfNode:
    def __init__(self, cond, body, ebody):
        self.cond = cond
        self.body = body
        self.ebody = ebody
        
    def eval(self, env):
        if self.cond.eval(env) != 0:
            for node in self.body:
                node.eval(env)
        else:
            for node in self.ebody:
                node.eval(env)
                
class WhileNode:
    def __init__(self, cond, body):
            self.cond = cond
            self.body = body
            
    def eval(self, env):
        while self.cond.eval(env) != 0:
            for node in self.body:
                node.eval(env) 