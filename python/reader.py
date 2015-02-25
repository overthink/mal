"Mal reader"
import re

class MalSymbol:
    """Represent a symbol in Mal."""
    def __init__(self, name):
        self.name = name

NIL = MalSymbol("nil")

class MalKeyword:
    """Represent a keyword in Mal."""
    def __init__(self, name):
        self.name = name

# compile this monster once
_tpattern = re.compile('''[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"|;.*|[^\s\[\]{}('"`,;)]*)''')
def tokenizer(s):
    "Returns a list of tokens in s."
    # TODO: if need be this can be changed to return an instance of a
    # Reader-like object with methods like next, peek, etc.
    return _tpattern.findall(s)

def read_list(tokens):
    "Reads tokens up to a ')' and return them all in a list."
    tokens.pop(0) # discard leading '('
    results = []
    while len(tokens) > 0:
        if tokens[0] == ')':
            tokens.pop(0)
            break
        results.append(read_form(tokens))
    return results

def read_string(token):
    "Read token as a string and return result."
    return token[1:-1]

_int_pattern = re.compile('''\d+''')
def read_atom(token):
    "Coerce token -- a string -- to appropriate type and return it."
    if _int_pattern.match(token):
        return int(token)
    elif token[0] == '"':
        return read_string(token)
    elif token[0] == ':':
        return MalKeyword(token)
    else:
        # symbol
        if token == "true":
            return True
        elif token == "false":
            return False
        elif token == "nil":
            # ? can nil just be a symbol?
            return NIL
        else:
            return MalSymbol(token)

def read_form(tokens):
    t = tokens[0]
    if len(t) > 0 and t[0] == '(':
        return read_list(tokens)
    else:
        tokens.pop(0)
        return read_atom(t)

def read_str(s):
    return read_form(tokenizer(s))

if __name__ == '__main__':
    ts = tokenizer('(foo true false bar Baz :xx :yyy (1 "xyz foo" 2 3 )\n  )')
    print read_form(ts)
    ts = tokenizer('(foo :yyy (1 nil 2 "string" 3))')
    print read_form(ts)
    print read_form(tokenizer('(1 "two" (33 :kw 44) nil my-sym)'))

