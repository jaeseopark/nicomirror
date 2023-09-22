from sqlalchemy import Column, String, ForeignKey, Boolean, Integer, Table
from sqlalchemy.orm import relationship

from nicomirror.db.impl.postgres.shared import Base

playlist_to_video_table = Table(
    "playlist_to_videos",
    Base.metadata,
    Column("playlist_id", ForeignKey("playlists.id"), primary_key=True),
    Column("video_id", ForeignKey("videos.id"), primary_key=True),
)

video_to_uploader_table = Table(
    "video_to_uploaders",
    Base.metadata,
    Column("video_id", ForeignKey("videos.id"), primary_key=True),
    Column("uploader_id", ForeignKey("uploaders.id"), primary_key=True),
)


class PlaylistDto(Base):
    __tablename__ = "playlists"

    id = Column(String(16), primary_key=True)
    name = Column(String(64), nullable=False)
    owner_id = Column(String(16), ForeignKey("uploaders.id"), nullable=False)
    is_monitored = Column(Boolean, nullable=False, index=True)
    videos = relationship("VideoDto", secondary=playlist_to_video_table, back_populates="playlists")
    last_updated = Column(Integer, nullable=False, default=0)


class VideoDto(Base):
    __tablename__ = 'videos'

    id = Column(String(16), primary_key=True)
    title = Column(String(256), nullable=False)
    views = Column(Integer, nullable=False)
    likes = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    is_accessible = Column(Boolean, nullable=False)
    timestamp = Column(Integer, nullable=False)
    thumbnail_url = Column(String(256), nullable=False)
    description = Column(String(4096), nullable=True)
    parent_video_id = Column(String(16), nullable=True, index=True)
    playlists = relationship("PlaylistDto", secondary=playlist_to_video_table, back_populates="videos")
    uploaders = relationship("UploaderDto", secondary=video_to_uploader_table, back_populates="videos")


class UploaderDto(Base):
    __tablename__ = "uploaders"

    id = Column(String(16), primary_key=True)
    names = relationship("UploaderNameDto", back_populates="uploader")
    videos = relationship("VideoDto", secondary=video_to_uploader_table, back_populates="uploaders")


class UploaderNameDto(Base):
    __tablename__ = "uploader_names"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uploader_id = Column(String(16), ForeignKey("uploaders.id"), nullable=False)
    name = Column(String(32), unique=True)
    uploader = relationship("UploaderDto", back_populates="names")
