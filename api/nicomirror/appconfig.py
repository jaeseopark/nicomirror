import pydash
import yaml

_DEFAULT = """
db:
  type: postgres
  postgres:
    host: db
    port: 5432
    db: nicomirror
    user: user
    password: changeme
cache:
  type: inmem
"""


# TODO: ability to override w/ environment variables
def get_app_config(override: dict = None) -> dict:
    default = yaml.safe_load(_DEFAULT)
    if override:
        return pydash.merge(default, override)
    return default
