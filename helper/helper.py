from functools import reduce

def maybe(func):
    def inner(*args):
        for arg in args:
            if isinstance(arg, Exception):
                return arg
        try:
            return func(*args)
        except Exception as e:
            return e
    return inner


def repeat(func, until):
    def inner(*args):
        result = func(*args)
        if until(result):
            return result
        return inner(*args)
    return inner

pipe = lambda *funcs: lambda arg: reduce(lambda acc, func: func(acc), funcs,arg)