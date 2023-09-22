import logging
from typing import List, Optional

import backoff
from nicoclient.model.playlist import Playlist
from nicoclient.model.video import Video

from sqlalchemy import create_engine, select, update
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, query

from nicomirror.db import Database
from nicomirror.db.impl.postgres.shared import Base
from nicomirror.db.impl.postgres.dto import PlaylistDto, UploaderDto, VideoDto
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

    def save_playlist(self, playlist: Playlist):
        with Session(self.engine) as session:
            # Upsert users
            uploader_dto = UploaderDto(id=playlist.owner_id)
            stmt = get_upsert_statement([uploader_dto])
            session.execute(stmt)

            # Upsert playlist
            playlist_dto = convert(playlist, to=PlaylistDto, override=dict(videos=[]))
            stmt = get_upsert_statement([playlist_dto])  # TODO: on conflict update
            session.execute(stmt)

            stmt = select(PlaylistDto).filter_by(id=playlist.id)
            playlist_dto = session.scalar(stmt)
            playlist_dto.videos = [convert(v, to=VideoDto) for v in playlist.videos]

            session.commit()

    def save_videos(self, videos: List[Video]):
        videos_dto = [convert(video, to=VideoDto) for video in videos]
        with Session(self.engine) as session:
            stmt = get_upsert_statement(videos_dto)
            session.execute(stmt)
            session.commit()

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
