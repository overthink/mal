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

while True:
    try:
        val = raw_input('user> ').rstrip()
        if len(val) > 0:
            print rep(val)
    except EOFError:
        print "Bye for now!"
        sys.exit(0)
    except reader.ReaderException as e:
        print "Error: " + str(e)

