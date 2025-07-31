import re
from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: str

class Lexer:
    
    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def _skip_ws(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def next_token(self) -> Token:
        self._skip_ws()
        if self.pos >= len(self.text):
            return Token("EOF", "")
        ch = self.text[self.pos]

        if ch == '+':
            self.pos += 1
            return Token("PLUS", "+")
     
        m = re.match(r'[A-Za-z_][A-Za-z_0-9]*', self.text[self.pos:])
        if m:
            lex = m.group(0)
            self.pos += len(lex)
            return Token("ID", lex)

        raise SyntaxError(f"Unknown character at position {self.pos}: {ch!r}")

    def tokenize(self):
        toks = []
        t = self.next_token()
        while t.type != "EOF":
            toks.append(t)
            t = self.next_token()
        toks.append(Token("EOF", ""))
        return toks

class Parser:
    def __init__(self, tokens, trace=True):
        self.tokens = tokens
        self.i = 0
        self.trace = trace
        self.depth = 0

    def _peek(self): return self.tokens[self.i]
    def _eat(self, kind):
        tok = self._peek()
        if tok.type == kind:
            if self.trace: print("  " * self.depth + f"match {kind} ({tok.value})")
            self.i += 1
            return tok
        raise SyntaxError(f"Expected {kind}, found {tok.type} ({tok.value})")

    def _log(self, msg):
        if self.trace: print("  " * self.depth + msg)

   
    def parse(self):
        self._log("parse -> E EOF")
        self.depth += 1
        self.E()
        self._eat("EOF")
        self.depth -= 1
        self._log("accept")

    def E(self):
        self._log("E -> T E'")
        self.depth += 1
        self.T()
        self.Ep()
        self.depth -= 1

    def Ep(self):
        tok = self._peek()
        if tok.type == "PLUS":
            self._log("E' -> + T E'")
            self.depth += 1
            self._eat("PLUS")
            self.T()
            self.Ep()
            self.depth -= 1
        else:
            self._log("E' -> ε")

    def T(self):
        self._log("T -> id")
        self.depth += 1
        self._eat("ID")
        self.depth -= 1


if __name__ == "__main__":
    
    text = "id + id + id"
    lexer = Lexer(text)
    tokens = lexer.tokenize()

    print("Tokens:", [(t.type, t.value) for t in tokens])
    print("\nTrace:")
    parser = Parser(tokens, trace=True)
    parser.parse()
    print("\n✓ Input accepted.")
