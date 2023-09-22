from nicomirror.db import Database
from nicomirror.db.impl.postgres import PostgresDatabase

_CLS_MAPPING = dict(
    postgres=PostgresDatabase
)


def get_db_instance(type: str, *args, **kwargs) -> Database:
    assert type in _CLS_MAPPING, f"INVALID_DATABASE_TYPE {type=} is not a valid database type"
    constructor = _CLS_MAPPING[type]
    return constructor(**kwargs[type])
