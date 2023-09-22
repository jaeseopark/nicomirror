from abc import ABC, abstractmethod
from typing import List

from nicoclient.model.playlist import Playlist
from nicoclient.model.video import Video


class Database(ABC):
    @abstractmethod
    def save_playlist(self, playlist: Playlist):
        pass

    @abstractmethod
    def save_videos(self, videos: List[Video]):
        pass

    @abstractmethod
    def get_video_by_id(self, video_id: str):
        pass

    @abstractmethod
    def get_playlist_by_id(self, playlist_id):
        pass
