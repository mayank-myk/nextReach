import abc
import os


class ConfigBackend(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_config(self, key, default=None):
        raise NotImplementedError("Not implemented")


class EnvironmentVariableConfigBackend(ConfigBackend):
    """
    Loads environment variables for config.
    >>> b = EnvironmentVariableConfigBackend()
    >>> import os
    >>> os.environ["foo"] = "bar"
    >>> b.get_config("foo")
    'bar'
    """

    def get_config(self, key, default=None):
        val = os.environ.get(key)
        if val is None or len(val) == 0:
            val = default
        return val


class DictConfigBackend(ConfigBackend):
    """
    Allows configuration of a backend based purely on a python dict.
    """

    def __init__(self, d):
        self.__d = d

    def get_config(self, key, default=None):
        return self.__d.get(key, default)


class ChainedConfigBackend(ConfigBackend):
    """
    Allows the use of multiple configs, trying each one in order for the variable.
    >>> b = ChainedConfigBackend([DictConfigBackend({'foo':'bar'}), DictConfigBackend({'buz':'baz', 'foo':'wrong'})])
    >>> b.get_config('foo')
    'bar'
    >>> b.get_config('buz')
    'baz'
    >>> b.get_config('missing')
    """

    def __init__(self, backends):
        self.__backends = backends

    def get_config(self, key, default=None):
        for b in self.__backends:
            val = b.get_config(key)
            if not ((val is None) or (len(val) == 0)):
                return val
        return default


class MissingConfigBackend(Exception):
    def __init__(self):
        super().__init__("Missing ConfigBackend")
