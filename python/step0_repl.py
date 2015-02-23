import sys

def READ(x):
    return x

def EVAL(x):
    return x

def PRINT(x):
    return x

def rep(x):
    return PRINT(EVAL(READ(x)))

while True:
    sys.stdout.write('> ')
    val = sys.stdin.readline()
    if val == '': break
    val = val.rstrip('\n')
    print rep(val)
