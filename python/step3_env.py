import sys
import readline
import traceback
import reader
import printer
from env import Env

class EvalException(Exception):
  """Won't cause the repl to crash, but aborts reading current form"""
  pass

def s(name):
    "Return a MalSymbol named s."
    return reader.MalSymbol(name)

REPL_ENV = Env(None)
REPL_ENV.set(s('+'), lambda a, b: a + b)
REPL_ENV.set(s('-'), lambda a, b: a - b)
REPL_ENV.set(s('*'), lambda a, b: a * b)
REPL_ENV.set(s('/'), lambda a, b: int(a/b))

def eval_ast(form, env):
    if isinstance(form, reader.MalSymbol):
        result = env.get(form)
        if result is None:
            raise EvalException('could not find symbol: ' + form.name)
        return result
    elif isinstance(form, reader.MalList):
        return [EVAL(x, env) for x in form.value]
    elif isinstance(form, list):
        return [EVAL(x, env) for x in form]
    elif isinstance(form, dict):
        result = {}
        for k, v in form.items():
            k0 = EVAL(k, env)
            v0 = EVAL(v, env)
            if result.has_key(k0):
                raise Exception("eval: key {0} appears more than once in map".format(k0))
            result[k0] = v0
        return result
    else:
        return form

def READ(s):
    return reader.read_str(s)

def EVAL(form, env):
    if isinstance(form, reader.MalList):
        first = form.value[0]
        if first == s('def!'):
            name = form.value[1]
            value = EVAL(form.value[2], env)
            env.set(name, value)
            return value
        elif first == s('let*'):
            # establish new lexical env
            inner_env = Env(env)
            bindings = form.value[1]
            # check for vector binding syntax
            if isinstance(bindings, reader.MalList):
                bindings = bindings.value
            expr = form.value[2]
            # iterate bindings, eval'ing and setting into new env
            for name, value in (bindings[pos:pos + 2] for pos in xrange(0, len(bindings), 2)):
                inner_env.set(name, EVAL(value, inner_env))
            return EVAL(expr, inner_env)
        elif first == s('quote'):
            return form
        else:
            # Function application
            evaluated = eval_ast(form, env)
            fn = evaluated[0]
            args = evaluated[1:]
            return fn(*args)
    else:
        return eval_ast(form, env)

def PRINT(form):
    return printer.pr_str(form)

def rep(x):
    return PRINT(EVAL(READ(x), REPL_ENV))

while True:
    try:
        val = raw_input('user> ').rstrip()
        if len(val) > 0:
            print rep(val)
    except EOFError:
        print "Bye for now!"
        sys.exit(0)
    except Exception as e:
        traceback.print_exc()

