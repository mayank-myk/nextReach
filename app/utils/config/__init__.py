from ..singleton import invoke_only_once
from .config_backend import (
    ConfigBackend,
    EnvironmentVariableConfigBackend,
    MissingConfigBackend,
)

_config_backend = EnvironmentVariableConfigBackend()


@invoke_only_once
def set_config_backend(backend):
    global _config_backend
    assert isinstance(
        backend, ConfigBackend
    ), "Config backend must be an instance of ConfigBackend"
    _config_backend = backend
    return None


def get_config(name, default=None):
    global _config_backend
    if _config_backend is None:
        raise MissingConfigBackend()
    return _config_backend.get_config(name, default=default)
