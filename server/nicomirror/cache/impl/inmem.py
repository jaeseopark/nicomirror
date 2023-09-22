import logging

from nicomirror.cache import NicoCache

logger = logging.getLogger("nicomirror")


class InMemCache(NicoCache):
    _dict = dict(
        videos=dict(),
        uploaders=dict(),
        playlists=dict()
    )

    def get_item(self, namespace: str, key: str):
        return self._dict[namespace].get(key)

    def set_item(self, namespace: str, key: str, value):
        self._dict[namespace][key] = value
        logger.debug(f"{namespace=} {key=} set")
