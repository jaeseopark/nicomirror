import logging
from time import time
from typing import List, Optional

import backoff
from nicoclient.model.playlist import Playlist
from nicoclient.model.uploader import Uploader
from nicoclient.model.video import Video
from sqlalchemy import create_engine, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from nicomirror.db import Database
from nicomirror.db.impl.postgres.dto import PlaylistDto, UploaderDto, VideoDto, UploaderNameDto, video_to_uploader_table
from nicomirror.db.impl.postgres.shared import Base
from nicomirror.db.impl.postgres.util import convert, get_upsert_statement

logger = logging.getLogger("nicomirror")


class PostgresDatabase(Database):
    def __init__(self, host, port, db, user, password, **kwargs):
        self.engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}")

        # 30 seconds timeout
        @backoff.on_exception(backoff.expo, OperationalError, max_time=30)
        def init_with_retry():
            Base.metadata.create_all(self.engine)

        init_with_retry()

    def get_video_by_id(self, video_id: str) -> Optional[Video]:
        with Session(self.engine) as session:
            video_dto = session.scalar(select(VideoDto).filter_by(id=video_id))
            if video_dto:
                return convert(video_dto, to=Video)

    def get_playlist_by_id(self, playlist_id) -> Optional[Playlist]:
        with Session(self.engine) as session:
            playlist_dto = session.scalar(select(PlaylistDto).filter_by(id=playlist_id))

            if playlist_dto:
                videos = [convert(v, to=Video, override=dict(playlists=[])) for v in playlist_dto.videos]
                return convert(playlist_dto, to=Playlist, override=dict(videos=videos))

    def get_uploader_by_id(self, uploader_id: str):
        with Session(self.engine) as session:
            return session.scalar(select(UploaderDto).filter_by(id=uploader_id))

    def get_recent_videos(self, limit: int):
        with Session(self.engine) as session:
            result = session.scalars(select(VideoDto).order_by(VideoDto.timestamp.desc()).limit(limit))
            return [convert(video, to=Video) for video in result]

    def save_uploader(self, uploader: Uploader):
        with Session(self.engine) as session:
            session.execute(get_upsert_statement(convert(uploader, to=UploaderDto, override=dict(names=[]))).on_conflict_do_nothing())
            uploader_dto = session.scalar(select(UploaderDto).filter_by(id=uploader.id))

            uploader_dto.names.clear()
            for name in uploader.names:
                name_dto = session.scalar(select(UploaderNameDto).filter_by(uploader_id=uploader.id, name=name))
                if not name_dto:
                    name_dto = UploaderNameDto(uploader_id=uploader.id, name=name)
                uploader_dto.names.append(name_dto)

            session.commit()

    def save_playlist(self, playlist: Playlist):
        with Session(self.engine) as session:
            # Upsert users
            uploader_dto = UploaderDto(id=playlist.owner_id, names=[])
            session.execute(get_upsert_statement([uploader_dto]).on_conflict_do_nothing())

            # Upsert playlist
            playlist_dto = convert(playlist, to=PlaylistDto, override=dict(videos=[]))
            # TODO: nice-to-have on conflict update
            session.execute(get_upsert_statement([playlist_dto]).on_conflict_do_nothing())

            # Associate videos to playlist
            playlist_dto = session.scalar(select(PlaylistDto).filter_by(id=playlist.id))
            playlist_dto.videos.clear()
            for video in playlist.videos:
                video_dto = session.scalar(select(VideoDto).filter_by(id=video.id))
                if not video_dto:
                    # Create a new VideoDto if not in DB
                    video_dto = convert(video, to=VideoDto)
                playlist_dto.videos.append(video_dto)

            # Update last updated timestamp
            playlist_dto.last_updated = int(time())

            session.commit()

    def save_videos(self, videos: List[Video]):
        with Session(self.engine) as session:
            videos_dto = [convert(video, to=VideoDto) for video in videos]
            session.execute(get_upsert_statement(videos_dto).on_conflict_do_nothing())
            session.commit()

    def link_video_to_uploader(self, video_id: str, uploader_id: str):
        with Session(self.engine) as session:
            session.execute(insert(UploaderDto).values(id=uploader_id).on_conflict_do_nothing())
            session.execute(insert(video_to_uploader_table).values(video_id=video_id, uploader_id=uploader_id).on_conflict_do_nothing())
            session.commit()

    def assign_parent(self, video_id: str, parent_video_id: str):
        stmt = update(VideoDto).where(VideoDto.id == video_id).values(parent_video_id=parent_video_id)
        with Session(self.engine) as session:
            session.execute(stmt)
            session.commit()
