import sys
import readline

def READ(x):
    return x

def EVAL(x):
    return x

def PRINT(x):
    return x

def rep(x):
    return PRINT(EVAL(READ(x)))

while True:
    val = raw_input('> ').rstrip()
    if len(val) > 0:
        print rep(val)

