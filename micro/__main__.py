import sys
from . import lexer
from . import parser
from . import nodes

# micro
# by las-r

# inbuilt functions
def ibtype(x):
    if isinstance(x, list): return "arr"
    if isinstance(x, float): return "float"
    if isinstance(x, nodes.Function) or callable(x): return "func"
    if isinstance(x, int): return "int"
    if isinstance(x, str): return "str"
    
def ibconv(x, t):
    if t == "arr": return list(x)
    if t == "float": return float(x)
    if t == "int": return int(x)
    if t == "str": return str(x)
    raise Exception(f"Unknown convertible type: {t}")

def ibadd(a, i, x):
    ac = a.copy()
    ac.insert(i, x)
    return ac

def ibdel(a, i):
    ac = a.copy()
    ac.pop(i)
    return ac

def main():
    if len(sys.argv) < 2:
        print("usage: python -m micro <file.mic>")
        return
    
    file = sys.argv[1]
    with open(file) as f:
        code = f.read()
        
    tokens = lexer.tokenize(code)
    nodes = parser.parse(tokens)
    
    env = {
        "print": print,
        "input": input,
        "type": ibtype,
        "conv": ibconv,
        "len": len,
        "add": ibadd,
        "del": ibdel
    }
    for node in nodes:
        node.eval(env)
        
if __name__ == "__main__":
    main()