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
        pass
    
class BinaryOpNode:
    def __init__(self, a, op, b):
        self.a = a
        self.op = op
        self.b = b
    
    def eval(self, env):
        pass