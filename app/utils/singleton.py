def singleton(f):
    """
    A decorator to allow a function to be a singleton. It must have no argument.
    :param f: a function with no arguments
    :return: function's return value.
    """
    s = []

    def ff():
        if len(s) == 0:
            s.append(f())
        return s[0]

    ff.__name__ = f.__name__
    return ff


def invoke_only_once(f):
    s = []

    def ff(*args, **kwargs):
        if len(s) == 0:
            s.append(f(*args, **kwargs))
        return s[0]

    ff.__name__ = f.__name__
    return ff


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
