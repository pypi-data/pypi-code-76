import math
import functools
import operator as op
import random
import traceback

from colored import attr, bg, fg
from termcolor import colored, cprint

import socket

from result import Ok, Err, OkErr

from .logger import logger, expression

import pdb

Symbol = str  # A Lisp Symbol is implemented as a Python str
List = list  # A Lisp List is implemented as a Python list
Int = int
Float = float


def unwrap(v):
    """Unwraps"""
    if isinstance(v, OkErr):
        return v.unwrap()
    return v


class Env(dict):
    """An environment: a dict of {'var':val} pairs, with an outer Env."""
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer
    def find(self, var):
        "Find the innermost Env where var appears."
        if var in self:
            return self
        elif self.outer is not None:
            return self.outer.find(var)

        raise Exception(f"Failed to find {var}")

class Procedure(object):
    """A user-defined Scheme procedure."""
    def __init__(self, parms, body, env, docs=""):
        self.parms, self.body, self.env = parms, body, env
        self.docs = docs
    def __call__(self, *args):
        return eval({}, self.body, env=Env(self.parms, args, outer=self.env))
    def __repr__(self):
        args = ','.join(self.parms)
        body = ' '.join([str(s) for s in self.body])
        return f"(Function ({args}) ({body}))"
    def doc(self):
        return (
f"""{self.docs}

args: {expression(self.parms)}

{expression(self.body)}""")

def standard_env():
    "Create an environment with some Scheme standard procedures."
    env = Env()
    env.update(vars(math))  # sin, cos, sqrt, pi, ...
    env.update(vars(functools))  # sin, cos, sqrt, pi, ...

    def unwrap_args(args):
        return (unwrap(arg) for arg in args)

    def last(*x):
        """Return the last element of a list."""
        x = unwrap_args(x)
        return (x[1],)

    def builtin_nth(x, y):
        """Get n element from list."""
        x,y = unwrap_args([x,y])
        return y[x]

    def car(x):
        """Return the first element of a list."""
        x = unwrap(x)
        return x[0]

    def cdr(*x):
        """Return the elements of a list except for the first one."""
        x = unwrap_args(x)
        return x[1:]

    def cons(x, y):
        """Return the list x and the element y at its tail."""
        x,y = unwrap_args([x,y])
        return x + [y]

    def _list(*x):
        """Return a list of arguments."""
        x = unwrap_args([x])
        return list(x)

    def list_pred(x):
        """Check if argument is a list."""
        x = unwrap_args([x])
        return isinstance(x, List)

    def null_pred(x):
        """Check if argument is null."""
        x = unwrap_args([x])
        return x == []

    def number_pred(x):
        """Check if argument is a number."""
        x,y = unwrap_args([x,y])
        return isinstance(x, Int) or isinstance(x, Float)

    def symbol_pred(x):
        """Check if argument is a symbol."""
        x = unwrap_args([x])
        return isinstance(x, Symbol)

    def builtin_plus(x, y):
        """Sum two numbers."""
        x,y = unwrap_args([x,y])
        return Ok(x + y)

    def builtin_sub(x,y):
        """Subtract two numbers."""
        x,y = unwrap_args([x,y])
        return Ok(x-y)

    def builtin_div(x,y):
        """Divide two numbers."""
        x,y = unwrap_args([x,y])
        return Ok(x/y)

    def builtin_pow(x,y):
        """Power of two numbers."""
        x,y = unwrap_args([x,y])
        return Ok(x**y)

    def builtin_gt(x,y):
        x,y = unwrap_args([x,y])
        return Ok(x>y)

    def builtin_lt(x,y):
        x,y = unwrap_args([x,y])
        return Ok(x<y)

    def builtin_ge(x,y):
        x,y = unwrap_args([x,y])
        return Ok(x>=y)

    def builtin_le(x,y):
        x,y = unwrap_args([x,y])
        return Ok(x<=y)

    def builtin_eq(x,y):
        x,y = unwrap_args([x,y])
        return Ok(x==y)

    def builtin_append(x, y):
        x,y = unwrap_args([x,y])
        return Ok(op.add(x,y))

    def cmd(env):
        return Procedure(
            ['dev', 'cmd', 'arg1', 'arg2', 'arg3'],
            ['builtin_cmd', 'dev', 'cmd', 'arg1', 'arg2', 'arg3'], env=env)

    def set(env):
        return Procedure(
            ['dev', 'cmd', 'value'],
            ['builtin_set', 'dev', 'cmd', 'value'], env=env)

    def get(env):
        return Procedure(
            ['dev', 'cmd'],
            ['builtin_get', 'dev', 'cmd'], env=env)

    def builtin_print(*args, **kwargs):
        """Python print function."""
        print(*args, **kwargs)
        return Ok()

    def unwrap(x):
        if x is OkErr:
            return x.unwrap()
        return x

    env.update(
        {
            "builtin_plus": builtin_plus,
            "+": Procedure(['x', 'y'], ['builtin_plus', 'x', 'y'], env=env, 
            docs="Same as a+b."),
            "builtin_sub": builtin_sub,
            "-": Procedure(['x', 'y'], ['builtin_sub', 'x', 'y'], env=env,
            docs="Same as a-b."),
            "*": op.mul,
            "builtin_div": builtin_div,
            "/": Procedure(['x', 'y'], ['builtin_div', 'x', 'y'], env=env,
            docs="Same as a/b."),
            "builtin_pow": builtin_pow,
            "**": Procedure(['x', 'y'], ['builtin_pow', 'x', 'y'], env=env,
            docs="Same as a**b."),
            "builtin_gt": builtin_gt,
            ">": Procedure(['x', 'y'], ['builtin_gt', 'x', 'y'], env=env,
            docs="Same as a > b."),
            "builtin_lt": builtin_lt,
            "<": Procedure(['x', 'y'], ['builtin_lt', 'x', 'y'], env=env,
            docs = "Same as a < b."),
            "builtin_ge": builtin_ge,
            ">=": Procedure(['x', 'y'], ['builtin_ge', 'x', 'y'], env=env, 
            docs="Same as a >= b."),
            "builtin_le": builtin_le,
            "<=": Procedure(['x', 'y'], ['builtin_le', 'x', 'y'], env=env, 
            docs="Same as a <= b."),
            "builtin_eq": builtin_eq,
            "=": Procedure(['x', 'y'], ['builtin_eq', 'x', 'y'], env=env, 
            docs = "Same as a == b."),
            "abs": abs,
            "builtin_append": builtin_append,
            "append": Procedure(['x', 'y'], ['builtin_append', 'x', 'y'], env=env,
            docs = "Appends an element y to the x list."),
            "last": last,
            "builtin_nth": builtin_nth,
            "nth": Procedure(['x', 'y'], ['builtin_nth', 'x', 'y'], env=env),
            "car": car,
            "cdr": cdr,
            "cons": cons,
            "eq?": op.is_,
            "equal?": op.eq,
            "length": len,
            "list": _list,
            "list?": list_pred,
            "map": map,
            "max": max,
            "min": min,
            "not": op.not_,
            "null?": null_pred,
            "number?": number_pred,
            "procedure?": callable,
            "round": round,
            "symbol?": symbol_pred,
            "print": builtin_print,
            "cmd": cmd(env),
            "set": set(env),
            "get": get(env),
            "unwrap": unwrap,
            "filter": filter,
        }
    )
    return env


global_env = standard_env()


def tokenize(s):
    """Convert a string into a list of tokens."""
    if s.startswith(";"):
        return []
    return s.replace("(", " ( ").replace(")", " ) ").split()


def atom(token):
    """Numbers become numbers; every other token is a symbol."""
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


def read_from_tokens(tokens):
    """Read tokens and construct ast."""
    if len(tokens) == 0:
        return None

    token = tokens.pop(0)
    if token == "(":
        L = []
        while tokens[0] != ")":
            L.append(read_from_tokens(tokens))
        tokens.pop(0)
        return L
    elif token == ")":
        raise SyntaxError("unexpected )")
    else:
        return atom(token)

def do(cfg, x, env):
    """Run multiple expressions."""
    _, *exps = x
    results = [eval(cfg, exp, env) for exp in exps]
    return results[-1]

def test(cfg, x, env):
    """Run test."""

    #pdb.set_trace()

    _, name, *exps = x
    results = [eval(cfg, exp, env) for exp in exps]

    for result in results:
        if result.is_err():
            logger.error(result.err())

    result = not any([exp.is_err() or exp.ok() == False for exp in results])
    logger.test(name, result)
    return result

def _assert(cfg, x, env):
    _, f_name, *exps = x
    results = [eval(cfg, exp, env) for exp in exps]
    for result in results:
        if type(result) is OkErr and result.is_err():
            return result

    f = eval(cfg, f_name, env)

    result = f(*results)
    logger.asserts(result, [f_name] + exps, [f_name] + results)
    return result


def eval(cfg, x, env=global_env, stack=[]):
    if isinstance(x, Symbol):
        if x[0] == '"':
            return x[1:-1]
        return env.find(x)[x]
    elif not isinstance(x, List):
        return Ok(x)
    elif isinstance(x, Int) or isinstance(x, Float):
        return Ok(x)

    op, *args = x
    if op == "do":
        return do(cfg, x, env)
    if op == "test":
        return test(cfg, x, env)
    elif op == "assert":
        return _assert(cfg, x, env)
    elif op == "exit":
        return "exit"
    elif op == "let":
        symbol, exp = args
        env[symbol] = eval(cfg, exp, env)
        return Ok(None)
    elif op == "lambda":
        parms, body = args
        return Ok(Procedure(parms, body, env))
    elif op == "def":
        symbol, parms, *rest = args
        body = []
        doc = ""
        if len(rest) == 1:
            body = rest[0]
        if len(rest) == 2:
            body, doc = rest

        env[symbol] = Procedure(parms, body, env, doc)
        return Ok(env[symbol])
    else:
        proc = unwrap(eval(cfg, op, env))
        # currying
        if isinstance(proc, Procedure) and len(proc.parms) > len(args):
            for i, arg in enumerate(args):
                env[proc.parms[i]] = eval(cfg, arg, env)
            return Procedure(proc.parms[len(args):], proc.body, env)
        elif isinstance(proc, Procedure):
            vals = [eval(cfg, arg, env) for arg in args]
            return proc(*vals)
        elif callable(proc):
            vals = [unwrap(eval(cfg, arg, env)) for arg in args]
            return proc(*vals)


class Program:
    def __init__(self, lines):
        self.lines = lines

    def take(self):
        open_count = close_count = 0
        acc = ""
        while len(self.lines) > 0:
            line = self.lines.pop(0)
            open_count += line.count("(")
            close_count += line.count(")")
            acc += line
            if open_count - close_count == 0:
                return acc

        return None


def rep(config, line):
    r = read_from_tokens(tokenize(line))
    if r is not None:
        try:
            r = eval(config, r)
        except Exception as e:
            traceback.print_exc()
            print(e)
            return
        if r == "exit":
            return "exit"
        return r


def parse(file, config):
    with open(file, "r") as f:
        program = Program(f.readlines())

    count = 0
    while True:
        line = program.take()
        if line is None:
            return count
        try:
            r = rep(config, line)
            if r is False:
                count += 1
        except Exception as e:
            traceback.print_exc()
            print("Parser Error:", e)

    return count

def printer(cfg, value):
    value = unwrap(value)
    if value is not None:
        print(value)
