"""MAL core functions."""
import reader

def s(name):
    "Return a MalSymbol named s."
    return reader.MalSymbol(name)

ns = {
    s('+'):      lambda a, b: a + b,
    s('-'):      lambda a, b: a - b,
    s('*'):      lambda a, b: a * b,
    s('/'):      lambda a, b: int(a/b),
    s('list'):   lambda *args: reader.MalList(list(args)),
    s('list?'):  lambda x: isinstance(x, reader.MalList),
    s('empty?'): lambda xs: len(xs) == 0,
    s('count'):  lambda xs: 0 if xs is None else len(xs),
    s('='):      lambda a, b: a == b,
    s('<'):      lambda a, b: a < b,
    s('<='):     lambda a, b: a <= b,
    s('>'):      lambda a, b: a > b,
    s('>='):     lambda a, b: a >= b
}

