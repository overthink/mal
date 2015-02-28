"Mal reader"
import re
import collections

class ReaderException(Exception):
  """Won't cause the repl to crash, but aborts reading current form"""
  pass

class MalList:
  """Just a wrapper for a normal python list so I can treat these differently
  than vectors, which will use the plain old list."""
  def __init__(self, value):
    self.value = value

class MalSymbol:
    """Represent a symbol in Mal."""
    def __init__(self, name):
        self.name = name
    def __lt__(self, other):
        return self.name.__lt__(other)
    def __hash__(self):
        return self.name.__hash__()
    def __eq__(self, other):
        return self.name.__eq__(other)

NIL = MalSymbol("nil")

class MalKeyword:
    """Represent a keyword in Mal."""
    def __init__(self, name):
        self.name = name
    def __lt__(self, other):
        return self.name.__lt__(other)
    def __hash__(self):
        return self.name.__hash__()
    def __eq__(self, other):
        return self.name.__eq__(other)

# compile this monster once
TOKEN_PATTERN = re.compile(r'''[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"|;.*|[^\s\[\]{}('"`,;)]+)''')
def tokenize(s):
    "Returns a list of tokens in s."
    # TODO: if need be this can be changed to return an instance of a
    # Reader-like object with methods like next, peek, etc.
    return TOKEN_PATTERN.findall(s)

def read_list(tokens):
    "Reads tokens up to a ')' and return them all in a MalList."
    tokens.pop(0) # discard leading '('
    results = []
    while len(tokens) > 0:
        if tokens[0] == ')':
            tokens.pop(0)
            break
        results.append(read_form(tokens))
    return MalList(results)

def read_vector(tokens):
    "Reads tokens up to a ']' and return them all in a list."
    tokens.pop(0) # discard leading '['
    results = []
    while len(tokens) > 0:
        if tokens[0] == ']':
            tokens.pop(0)
            break
        results.append(read_form(tokens))
    return results

def read_map(tokens):
    "Reads tokens up to a '}' and return them all in a list."
    tokens.pop(0) # discard leading '{'
    result = {}
    while len(tokens) > 0:
        if tokens[0] == '}':
            tokens.pop(0)
            break
        key = read_form(tokens)
        if not isinstance(key, collections.Hashable):
            raise Exception(str(type(key)) + " is not hashable and cannot be a map key")
        if result.has_key(key):
            raise Exception("key {0} appears more than once in map".format(key))
        if tokens[0] == '}':
            raise Exception("maps must have even number of elements")
        value = read_form(tokens)
        result[key] = value
    return result

def read_string(token):
    "Read token as a string and return result."
    return token[1:-1].decode('string_escape')

_int_pattern = re.compile('''\d+''')
def read_atom(token):
    "Coerce token -- a string -- to appropriate type and return it."
    assert len(token) > 0
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

# Reader dispatch
DISP = {"'": 'quote',
        '`': 'quasiquote',
        '~': 'unquote',
        '@': 'deref',
        '~@': 'splice-unquote'}

def read_form(tokens):
    if len(tokens) == 0:
        return NIL
    t = tokens[0]
    assert len(t) > 0

    if t[0] == '(':
        return read_list(tokens)
    if t[0] == '[':
        return read_vector(tokens)
    if t[0] == '{':
        return read_map(tokens)

    disp_val = DISP.get(t)
    if disp_val is not None:
        tokens.pop(0) # discard dispatch token
        quoted = read_form(tokens) # read next form
        return MalList([MalSymbol(disp_val), quoted])
    elif t == '^':
        tokens.pop(0) # discard ^
        meta = read_form(tokens)
        value = read_form(tokens)
        return MalList([MalSymbol('with-meta'), value, meta])
    else:
        return read_atom(tokens.pop(0))

def read_str(s):
    "Read s and return a list of forms read from it."
    tokens = tokenize(s)
    form = read_form(tokens)
    #if len(tokens) > 0:
    #  raise ReaderException('trailing tokens: ' + repr(tokens))
    return form

if __name__ == '__main__':
    #ts = tokenize('(foo true false bar Baz :xx :yyy (1 "xyz foo" 2 3 )\n  )')
    #print read_form(ts)
    #ts = tokenize('(foo :yyy (1 nil 2 "string" 3))')
    #print read_form(ts)
    #print read_form(tokenize('(1 "two" (33 :kw 44) nil my-sym)'))
    print tokenize("(def x 42) ; comment!")
    print tokenize('')
    print tokenize('(A b) (c d)')

