import logging

import nicoclient

from nicomirror.appconfig import get_app_config
from nicomirror.cache.factory import get_cache_instance
from nicomirror.db.factory import get_db_instance
from nicomirror.nicomirror import NicoMirror

LOG_FORMAT = "%(levelname)s %(asctime)s %(module)s %(funcName)s:%(lineno)d\t%(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger("nicomirror")
logger.setLevel(logging.INFO)


def get_mirror_instance() -> NicoMirror:
    app_config = get_app_config()
    cache = get_cache_instance(**app_config["cache"])
    db = get_db_instance(**app_config["db"])

    return NicoMirror(cache=cache, db=db,
                      video_getter=nicoclient.get_video_by_id,
                      playlist_getter=nicoclient.get_playlist,
                      utattemita_video_getter=nicoclient.search_utattemita_videos)
