import logging
from dataclasses import dataclass
from typing import Callable, List

from nicoclient.model.playlist import Playlist
from nicoclient.model.video import Video

from nicomirror.cache import NicoCache
from nicomirror.db import Database

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

    def get_video_by_id(self, video_id: str, force_fetch=False) -> Video:
        # TODO use regex for ID validation
        assert video_id.startswith("sm") or video_id.startswith("nm"), "video_id must start with 'sm' or 'nm'."

        if not force_fetch and video_id in self.cache.videos:
            return self.cache.videos[video_id]

        video = self.db.get_video_by_id(video_id)
        if force_fetch or not video:
            logger.info(f"VIDEO_CACHE_MISS {video_id=}")
            video = self.video_getter(video_id)
            self.db.save_videos([video])

        self.cache.videos[video_id] = video
        return video

    def get_playlist_by_id(self, playlist_id: str, force_fetch=False) -> Playlist:
        assert playlist_id.isdigit(), "playlist_id must be all-numeric."

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

    def get_utattemita_videos_by_id(self, video_id: str) -> List[Video]:
        videos = self.utattemita_video_getter(video_id)
        self.db.save_videos(videos)
        for video in videos:
            self.cache.videos[video.id] = video
        return videos
