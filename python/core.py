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

def do_println(print_readably, args):
    first = True
    for form in args:
        if not first:
            sys.stdout.write(' ')
        first = False
        sys.stdout.write(printer.pr_str(form, print_readably))
    print('')

def println(*args):
    return do_println(False, args)

def prn(*args):
    return do_println(True, args)

ns = {
    s('+'):       lambda a, b: a + b,
    s('-'):       lambda a, b: a - b,
    s('*'):       lambda a, b: a * b,
    s('/'):       lambda a, b: int(a/b),
    s('list'):    lambda *args: reader.MalList(list(args)),
    s('list?'):   lambda x: isinstance(x, reader.MalList),
    s('empty?'):  lambda xs: len(xs) == 0,
    s('count'):   lambda xs: 0 if xs is None else len(xs),
    s('='):       lambda a, b: a == b,
    s('<'):       lambda a, b: a < b,
    s('<='):      lambda a, b: a <= b,
    s('>'):       lambda a, b: a > b,
    s('>='):      lambda a, b: a >= b,
    s('not'):     lambda x: falsey(x),
    s('println'): println,
    s('prn'):     prn,
    s('pr-str'):  println,
    s('str'):     println
}

