"""MAL core functions."""
import sys
import reader
import printer

def falsey(x):
    "false and nil are logical false, all else is logically true."
    # remember that False == 0 in python... and in Mal 0 is truthy
    return (isinstance(x, bool) and x == False) or x == reader.NIL

def truthy(x):
    return not(falsey(x))

def s(name):
    "Return a MalSymbol named s."
    return reader.MalSymbol(name)

def str(*args):
    strs = []
    for form in args:
        strs.append(printer.pr_str(form, print_readably = False))
    return ''.join(strs)

def pr_str(*args):
    strs = []
    for form in args:
        strs.append(printer.pr_str(form, print_readably = True))
    return ' '.join(strs)

def do_println(print_readably, args):
    first = True
    for form in args:
        if not first:
            sys.stdout.write(' ')
        first = False
        sys.stdout.write(printer.pr_str(form, print_readably))
    print('')
    return reader.NIL

def println(*args):
    return do_println(False, args)

def prn(*args):
    return do_println(True, args)

def slurp(filename):
    "Return contents of filename as string."
    with open(filename, 'r') as f:
        return f.read()

ns = {
    s('+'):           lambda a, b: a + b,
    s('-'):           lambda a, b: a - b,
    s('*'):           lambda a, b: a * b,
    s('/'):           lambda a, b: int(a/b),
    s('list'):        lambda *args: reader.MalList(list(args)),
    s('list?'):       lambda x: isinstance(x, reader.MalList),
    s('empty?'):      lambda xs: len(xs) == 0,
    s('count'):       lambda xs: 0 if xs is None else len(xs),
    s('='):           lambda a, b: a == b,
    s('<'):           lambda a, b: a < b,
    s('<='):          lambda a, b: a <= b,
    s('>'):           lambda a, b: a > b,
    s('>='):          lambda a, b: a >= b,
    s('println'):     println,
    s('prn'):         prn,
    s('pr-str'):      pr_str,
    s('str'):         str,
    s('read-string'): reader.read_str,
    s('slurp'):       slurp
}

