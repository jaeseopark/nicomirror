import logging
from dataclasses import dataclass
from typing import Callable, List

from nicoclient.model.playlist import Playlist
from nicoclient.model.video import Video

from nicomirror.cache import NicoCache
from nicomirror.db import Database
from nicomirror.decorators import validate_video_ids, validate_playlist_ids

logger = logging.getLogger("nicomirror")


@dataclass
class NicoMirror:
    cache: NicoCache
    db: Database
    video_getter: Callable[[str], Video]
    playlist_getter: Callable[[str], Playlist]
    utattemita_video_getter: Callable[[str], List[Video]]

    def get_trending_videos(self) -> List[Video]:
        raise NotImplementedError

    def get_recent_videos(self, limit:int):
        return self.db.get_recent_videos(limit=limit)

    @validate_video_ids("video_id")
    def get_video_by_id(self, video_id: str, force_fetch=False) -> Video:
        if not force_fetch and video_id in self.cache.videos:
            return self.cache.videos[video_id]

        video = self.db.get_video_by_id(video_id)
        if force_fetch or not video:
            logger.info(f"VIDEO_CACHE_MISS {video_id=}")
            video = self.video_getter(video_id)
            self.db.save_videos([video])
            video = self.db.get_video_by_id(video.id)

        self.cache.videos[video_id] = video
        return video

    @validate_playlist_ids("playlist_id")
    def get_playlist_by_id(self, playlist_id: str, force_fetch=False) -> Playlist:
        if not force_fetch and playlist_id in self.cache.playlists:
            return self.cache.playlists[playlist_id]

        playlist = self.db.get_playlist_by_id(playlist_id)
        if force_fetch or not playlist:
            logger.info(f"PLAYLIST_CACHE_MISS {playlist_id=}")
            playlist = self.playlist_getter(playlist_id)
            self.db.save_playlist(playlist)

        self.cache.playlists[playlist_id] = playlist
        for video in playlist.videos:
            self.cache.videos[video.id] = video
        return playlist

    @validate_video_ids("video_id")
    def get_utattemita_videos_by_id(self, video_id: str) -> List[Video]:
        videos = self.utattemita_video_getter(video_id)
        if len(videos) > 0:
            self.db.save_videos(videos)
            videos = [self.db.get_video_by_id(v.id) for v in videos]
        for video in videos:
            self.cache.videos[video.id] = video
        return videos

    @validate_video_ids(["video_id", "parent_video_id"])
    def assign_parent(self, video_id, parent_video_id) -> Video:
        self.db.assign_parent(video_id, parent_video_id)
        video = self.db.get_video_by_id(video_id)
        self.cache.videos[video.id] = video
        return video
