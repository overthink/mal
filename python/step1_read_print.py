import sys
import readline
import reader
import printer

def READ(form):
    return reader.read_str(form)

def EVAL(x):
    return x

def PRINT(form):
    return printer.pr_str(form)

def rep(x):
    return PRINT(EVAL(READ(x)))

try:
    while True:
        val = raw_input('user> ').rstrip()
        if len(val) > 0:
            print rep(val)
except EOFError:
    print "^D"
    sys.exit(0)

