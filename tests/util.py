from collections import namedtuple
from inspect import getargspec


def inspect_function_args(func):
    args, _, _, defaults = getargspec(func)

    # remove 'self' if present
    if len(args) > 0 and args[0] == 'self':
        args.pop(0)

    # if no keywords then 'defaults' is None
    # so initialize to empty list
    defaults = defaults or list()

    nkws = len(defaults)
    offset = len(args)-nkws
    arguments = args[:offset]
    keywords_names = args[offset:]
    keywords = dict(zip(keywords_names, defaults))

    result = namedtuple('function_args', ['args', 'keywords'])
    return result(args=arguments, keywords=keywords)
