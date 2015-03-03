import sys
import readline
import reader
import printer

class EvalException(Exception):
  """Won't cause the repl to crash, but aborts reading current form"""
  pass

REPL_ENV = {reader.MalSymbol('+'): lambda a, b: a + b,
            reader.MalSymbol('-'): lambda a, b: a - b,
            reader.MalSymbol('*'): lambda a, b: a * b,
            reader.MalSymbol('/'): lambda a, b: int(a/b)}

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
            result[EVAL(k, env)] = EVAL(v, env)
        return result
    else:
        return form

def READ(s):
    return reader.read_str(s)

def EVAL(form, env):
    if isinstance(form, reader.MalList):
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
        print "Error: " + str(e)

