import logging
from typing import List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.orm.collections import InstrumentedList

from nicomirror.db.impl.postgres.shared import Base

logger = logging.getLogger("nicomirror")


def convert(source_object, to: type, override: dict = None):  # convert to and from DTO/BaseModel
    def get_allowed_keys():
        if issubclass(to, Base):
            return {k for k, v in vars(to).items() if isinstance(v, InstrumentedAttribute)}
        return set(vars(to)["model_fields"].keys())

    allowed_keys = get_allowed_keys()

    kwargs = {k: v for k, v in vars(source_object).items() if k in allowed_keys}
    kwargs.update(override or dict())

    return to(**kwargs)


def get_upsert_statement(dtos: List[Base]):
    def to_dict(dto):
        return {k: v for k, v in vars(dto).items() if not k.startswith("_") and not isinstance(v, InstrumentedList)}

    return insert(type(dtos[0])).values([to_dict(dto) for dto in dtos])
