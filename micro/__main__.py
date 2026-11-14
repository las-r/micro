import os
import sys
import micro.lexer
import micro.parser
import micro.nodes

# micro
# by las-r

# constants
TYPES = {"arr": list, "float": float, "int": int, "str": str}

# inbuilt functions
def ibtype(x):
    if isinstance(x, micro.nodes.Function) or callable(x): return "func"
    return {v: k for k, v in TYPES.items()}[type(x)]
    
def ibconv(x, t):
    if t in TYPES:
        return TYPES[t](x)
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
        
    tokens = micro.lexer.tokenize(code)
    nodes = micro.parser.parse(tokens)
    
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
        node.eval(env, [os.path.abspath(file)])
        
if __name__ == "__main__":
    main()