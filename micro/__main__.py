import os
import sys
import micro.lexer
import micro.parser
import micro.nodes

# micro
# by las-r

# constants
TYPES = {"arr": list, "float": float, "int": int, "str": str}
TYPENAMES = {v: k for k, v in TYPES.items()}
ANY = object()

# typename helper
def typename(x):
    if isinstance(x, micro.nodes.Function) or callable(x): return "func"
    return TYPENAMES.get(type(x), type(x).__name__)

# builtin decorator
def builtin(*sig):
    def deco(fn):
        def wrapper(*args):
            if len(args) != len(sig):
                raise Exception(f"{fn.__name__}() takes {len(sig)} argument(s), got {len(args)}")
            for i, (a, t) in enumerate(zip(args, sig)):
                if t is ANY:
                    continue
                ts = t if isinstance(t, tuple) else (t,)
                if isinstance(a, bool) or not isinstance(a, ts):
                    names = "/".join(TYPENAMES[x] for x in ts)
                    raise Exception(f"{fn.__name__}() argument {i + 1} must be {names}, got {typename(a)}")
            return fn(*args)
        wrapper.__name__ = fn.__name__
        return wrapper
    return deco

# inbuilt functions
@builtin(ANY)
def ibprint(x):
    print(x)

@builtin(str)
def ibinput(p):
    return input(p)

@builtin(ANY)
def ibtype(x):
    return typename(x)

@builtin(ANY, str)
def ibconv(x, t):
    if t in TYPES:
        return TYPES[t](x)
    raise Exception(f"Unknown convertible type: {t}")

@builtin((str, list))
def iblen(a):
    return len(a)

@builtin(list, int, ANY)
def ibadd(a, i, x):
    ac = a.copy()
    ac.insert(i, x)
    return ac

@builtin(list, int)
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