import re

# micro lexer
# by las-r

# regex pattern
REGEX = re.compile(r"""
    (?P<COMMENT>  //[^\n]*) |
    (?P<NUMBER>   \d+(?:\.\d+)?) |
    (?P<STRING>   "(?:\\.|[^"\\])*") |
    (?P<KEYWORD>  \b(if|end|while|func|break|return)\b) |
    (?P<OPER>     ==|!=|<=|>=|[+\-*/<>~&^():=,]) |
    (?P<IDENT>    [a-zA-Z_]\w*) |
    (?P<SKIP>     [ \t\r\n]+) |
    (?P<MISMATCH> .)
""", re.VERBOSE)

# tokens class
class Tokens:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0
        
    def can_eat(self, inc=1):
        return self.i < len(self.tokens) - inc
        
    def eat(self, inc=1):
        self.i += inc
        return self.tokens[self.i - inc]
    
    def peek(self, off=0):
        return self.tokens[self.i + off]
    
# tokenizer
def tokenize(code):
    tokens = []
    for match in REGEX.finditer(code):
        typ = match.lastgroup
        val = match.group()
        if typ in ("SKIP", "COMMENT"):
            continue
        elif typ == "MISMATCH":
            raise SyntaxError(f"Unexpected token: {val}")
        tokens.append(val)
    return Tokens(tokens)