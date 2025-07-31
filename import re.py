import re
keywords = {'if', 'else', 'while', 'for', 'return', 'int', 'float', 'char', 'void'}
operators = {'+', '-', '*', '/', '=', '==', '!=', '<', '<=', '>', '>='}
delimiters = {'(', ')', '{', '}', '[', ']', ';', ',', '.'}

identifier_pattern = r'[a-zA-Z_][a-zA-Z_0-9]*'
number_pattern = r'\d+'

def lexical_analyzer(code):
    tokens = []
    token_list = re.findall(r'\w+|==|!=|<=|>=|[^\s]', code)

    for token in token_list:
        if token in keywords:
            tokens.append((token, "KEYWORD"))
        elif token in operators:
            tokens.append((token, "OPERATOR"))
        elif token in delimiters:
            tokens.append((token, "DELIMITER"))
        elif re.fullmatch(number_pattern, token):
            tokens.append((token, "NUMBER"))
        elif re.fullmatch(identifier_pattern, token):
            tokens.append((token, "IDENTIFIER"))
        else:
            tokens.append((token, "UNKNOWN"))
    
    return tokens

code = "int a = b + 5; if (a > 10) return a;"

tokens = lexical_analyzer(code)

print("Lexical Analysis Result:")
for tok, tok_type in tokens:
    print(f"{tok:<10} --> {tok_type}")
