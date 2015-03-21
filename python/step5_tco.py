import sys
import readline
import traceback
import reader
import printer
import core
import types
from env import Env

class EvalException(Exception):
  """Won't cause the repl to crash, but aborts reading current form"""
  pass

def s(name):
    "Return a MalSymbol named s."
    return reader.MalSymbol(name)

REPL_ENV = Env(None, [], [])
for sym, fn in core.ns.items():
    REPL_ENV.set(sym, fn)

def eval_ast(ast, env):
    if isinstance(ast, reader.MalSymbol):
        result = env.get(ast)
        if result is None:
            raise EvalException('could not find symbol: ' + ast.name)
        return result
    elif isinstance(ast, reader.MalList):
        return [EVAL(x, env) for x in ast.value]
    elif isinstance(ast, list):
        return [EVAL(x, env) for x in ast]
    elif isinstance(ast, dict):
        result = {}
        for k, v in ast.items():
            k0 = EVAL(k, env)
            v0 = EVAL(v, env)
            if result.has_key(k0):
                raise Exception("eval: key {0} appears more than once in map".astat(k0))
            result[k0] = v0
        return result
    else:
        return ast

def READ(s):
    return reader.read_str(s)

def EVAL(ast, env):
    while True:
        if isinstance(ast, reader.MalList):
            first = ast.value[0]
            if first == s('def!'):
                name = ast.value[1]
                value = EVAL(ast.value[2], env)
                env.set(name, value)
                return value
            elif first == s('let*'):
                # establish new lexical env
                inner_env = Env(env, [], [])
                bindings = ast.value[1]
                # check for vector binding syntax
                if isinstance(bindings, reader.MalList):
                    bindings = bindings.value
                expr = ast.value[2]
                # iterate bindings, eval'ing and setting into new env
                for name, value in (bindings[pos:pos + 2] for pos in xrange(0, len(bindings), 2)):
                    inner_env.set(name, EVAL(value, inner_env))
                env = inner_env
                ast = expr
            elif first == s('do'):
                exprs = ast.value[1:]
                if len(exprs) == 0:
                    ast = reader.NIL
                else:
                    eval_ast(exprs[:-1], env)
                    ast = exprs[-1]
            elif first == s('if'):
                args = ast.value[1:]
                if len(args) < 2:
                    raise Exception("need 2 or 3 args for if")
                if len(args) == 2:
                    # if no then clause, use nil
                    args.append(reader.NIL)
                cond, then, else_ = args
                cond_e = EVAL(cond, env)
                if core.truthy(cond_e):
                    ast = then
                else:
                    ast = else_
            elif first == s('fn*'):
                params = ast.value[1]
                body = ast.value[2]
                def closure(*args):
                    inner = Env(env, params, list(args))
                    return EVAL(body, inner)
                return reader.MalFn(closure, body, params, env)
            elif first == s('quote'):
                return ast
            else:
                # Function application
                evaluated = eval_ast(ast, env)
                fn = evaluated[0]
                args = evaluated[1:]
                if isinstance(fn, types.FunctionType):
                    return fn(*args)
                elif isinstance(fn, reader.MalFn):
                    # TCO
                    ast = fn.ast
                    env = Env(fn.env, fn.params, args)
                else:
                    raise EvalException("unexpected fn type: {0}".format(fn))
        else:
            return eval_ast(ast, env)

def PRINT(form):
    return printer.pr_str(form)

def rep(x):
    return PRINT(EVAL(READ(x), REPL_ENV))

while True:
    rep('(def! not (fn* [x] (if x false true)))')
    try:
        val = raw_input('user> ').rstrip()
        if len(val) > 0:
            print rep(val)
    except EOFError:
        print "Bye for now!"
        sys.exit(0)
    except Exception as e:
        traceback.print_exc(file=sys.stderr)

