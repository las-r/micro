import sys
from . import lexer
from . import parser

# micro
# by las-r

def main():
    if len(sys.argv) < 2:
        print("usage: python -m micro <file.mic>")
        return
    
    file = sys.argv[1]
    with open(file) as f:
        code = f.read()
        
    tokens = lexer.tokenize(code)
    node = parser.parseexpr(tokens)
    print(node.eval({}))
        
if __name__ == "__main__":
    main()