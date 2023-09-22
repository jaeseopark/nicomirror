from nicomirror.cache import NicoCache
from nicomirror.cache.impl.inmem import InMemCache

_CLS_MAPPING = dict(
    inmem=InMemCache
)


def get_cache_instance(type: str, *args, **kwargs) -> NicoCache:
    assert type in _CLS_MAPPING, f"INVALID_CACHE_TYPE {type=} is not a valid cache type"
    constructor = _CLS_MAPPING[type]
    return constructor(*args, **kwargs)
