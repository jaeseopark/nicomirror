from abc import ABC, abstractmethod
from typing import List, Optional

from nicoclient.model.playlist import Playlist
from nicoclient.model.uploader import Uploader
from nicoclient.model.video import Video


class Database(ABC):
    @abstractmethod
    def get_video_by_id(self, video_id: str) -> Optional[Video]:
        pass

    @abstractmethod
    def get_playlist_by_id(self, playlist_id) -> Optional[Playlist]:
        pass

    @abstractmethod
    def get_uploader_by_id(self, uploader_id: str) -> Optional[Uploader]:
        pass

    @abstractmethod
    def save_uploader(self, uploader: Uploader):
        """
        Userts the given uploader
        :param uploader: Uploader to upsert
        :return: None
        """
        pass

    @abstractmethod
    def save_playlist(self, playlist: Playlist):
        pass

    @abstractmethod
    def save_videos(self, videos: List[Video]):
        pass

    @abstractmethod
    def link_video_to_uploader(self, video_id: str, uploader_id: str):
        """
        Links an uploader to an existing video
        :param video_id: ID of an existing video
        :param uploader_id: ID of an uploader who may or may not exist in the database
        :return: None
        """
        pass

    @abstractmethod
    def get_recent_videos(self, limit: int):
        pass

    @abstractmethod
    def assign_parent(self, video_id: str, parent_video_id: str):
        pass
