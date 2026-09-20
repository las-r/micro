import os

# micro nodes
# by las-r

# exceptions
class Break(Exception):
    pass

class Return(Exception):
    def __init__(self, value):
        self.value = value

# function object
class Function:
    def __init__(self, params, body, env):
        self.params = params
        self.body = body
        self.env = env

# literal node
class LiteralNode:
    def __init__(self, value):
        self.value = value
    
    def eval(self, env, paths=None):
        return self.value

# variable nodes
class VariableNode:
    def __init__(self, name):
        self.name = name
    
    def eval(self, env, paths=None):
        if self.name in env:
            return env[self.name]
        raise Exception(f"Undefined variable: {self.name}")

class AssignNode:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def eval(self, env, paths=None):
        val = self.expr.eval(env)
        if isinstance(val, list):
            val = val.copy()
        env[self.name] = val
    
# operation nodes
class UnaryOpNode:
    def __init__(self, op, a):
        self.op = op
        self.a = a
    
    def eval(self, env, paths=None):
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
    
    def eval(self, env, paths=None):
        a = self.a.eval(env)
        if self.op == "&&": return int(a and self.b.eval(env))
        if self.op == "||": return int(a or self.b.eval(env))
        b = self.b.eval(env)
        if self.op == "+": return a + b
        if self.op == "-": return a - b
        if self.op == "*": return a * b
        if self.op == "/": return a / b
        if self.op == "%": return a % b
        if self.op == "&": return a & b
        if self.op == "|": return a | b
        if self.op == "^": return a ^ b
        if self.op == "==": return int(a == b)
        if self.op == "<=": return int(a <= b)
        if self.op == ">=": return int(a >= b)
        if self.op == "<": return int(a < b)
        if self.op == ">": return int(a > b)
        raise Exception(f"Unknown binary operator: {self.op}")
    
# array nodes
class ArrayNode:
    def __init__(self, items):
        self.items = items
        
    def eval(self, env, paths=None):
        return [i.eval(env) for i in self.items]
    
class IndexNode:
    def __init__(self, arr, idx):
        self.arr = arr
        self.idx = idx
        
    def eval(self, env, paths=None):
        arr = self.arr.eval(env)
        idx = self.idx.eval(env)
        return arr[idx]
    
class IndexAssignNode:
    def __init__(self, arr, idx, val):
        self.arr = arr
        self.idx = idx
        self.val = val
    
    def eval(self, env, paths=None):
        arr = self.arr.eval(env)
        idx = self.idx.eval(env)
        val = self.val.eval(env)
        arr[idx] = val
    
# control flow nodes
class IfNode:
    def __init__(self, cond, body, ebody):
        self.cond = cond
        self.body = body
        self.ebody = ebody
        
    def eval(self, env, paths=None):
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
            
    def eval(self, env, paths=None):
        try:
            while self.cond.eval(env) != 0:
                for node in self.body:
                    node.eval(env)
        except Break:
            pass
        
class BreakNode:
    def __init__(self):
        pass
    
    def eval(self, env, paths=None):
        raise Break
    
# function nodes
class FunctionNode:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body
    
    def eval(self, env, paths=None):
        env[self.name] = Function(self.params, self.body, env.copy())
        
class CallNode:
    def __init__(self, name, args):
        self.name, self.args = name, args

    def eval(self, env, paths=None):
        if self.name not in env:
            raise Exception(f"Undefined function: {self.name}")
        func = env[self.name]
        copy = lambda v: v.copy() if isinstance(v, list) else v
        eargs = [a.eval(env) for a in self.args]
        if callable(func):
            return func(*[copy(a) for a in eargs])
        if isinstance(func, Function):
            if len(self.args) != len(func.params):
                raise Exception(f"Argument mismatch for {self.name}")
            lenv = func.env | {p: copy(v) for p, v in zip(func.params, eargs)}
            try:
                for node in func.body: 
                    node.eval(lenv)
            except Return as e:
                return e.value
        raise Exception(f"'{self.name}' is not a callable function")
    
class ReturnNode:
    def __init__(self, expr):
        self.expr = expr
        
    def eval(self, env, paths=None):
        raise Return(self.expr.eval(env) if self.expr else None)
    
# import nodes
class ImportNode:
    def __init__(self, path):
        self.path = path

    def eval(self, env, paths):
        from . import lexer
        from . import parser
        fpath = os.path.abspath(
            os.path.join(os.path.dirname(paths[-1]), self.path.eval(env))
        )
        if fpath in paths:
            raise Exception(f"Circular import: {fpath}")
        paths.append(fpath)
        with open(fpath) as f:
            code = f.read()
        tokens = lexer.tokenize(code)
        nodes = parser.parse(tokens)
        for node in nodes:
            node.eval(env, paths)
        paths.pop()