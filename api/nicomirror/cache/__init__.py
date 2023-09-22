from abc import ABC, abstractmethod


class CacheNamespace:
    def __init__(self, parent, namespace: str):
        self.parent = parent
        self.namespace = namespace

    def __getitem__(self, key):
        return self.parent.get_item(self.namespace, key)

    def __setitem__(self, key, value):
        return self.parent.set_item(self.namespace, key, value)

    def __contains__(self, key):
        # Note: None always means a cache miss because it is not a valid cacheable value.
        # If None was a valid value, then I wouldn't be able to use the following expression.
        return self.parent.get_item(self.namespace, key) is not None


class NicoCache(ABC):
    def __init__(self):
        self.playlists = CacheNamespace(self, "playlists")
        self.videos = CacheNamespace(self, "videos")
        self.uploaders = CacheNamespace(self, "uploaders")

    @abstractmethod
    def get_item(self, namespace: str, key: str):
        pass

    @abstractmethod
    def set_item(self, namespace: str, key: str, value):
        pass
