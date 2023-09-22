from fastapi import FastAPI
from starlette.responses import JSONResponse

from nicomirror.factory import get_mirror_instance
from nicoclient.model.playlist import Playlist
from nicoclient.model.video import Video

app = FastAPI()
mirror = get_mirror_instance()


@app.exception_handler(AssertionError)
def unicorn_exception_handler(_, e: AssertionError):
    return JSONResponse(
        status_code=400,
        content=dict(message=str(e))
    )


@app.exception_handler(NotImplementedError)
def unicorn_exception_handler(*args, **kwargs):
    return JSONResponse(
        status_code=500,
        content=dict(message="Not implemented")
    )


@app.get("/")
def root():
    return dict(
        trending_videos=mirror.get_trending_videos()
    )


@app.get("/videos/{video_id}", response_model=Video)
def get_video_by_id(video_id):
    return mirror.get_video_by_id(video_id)


@app.get("/videos/{video_id}/utattemita")
def get_utattemita_videos_by_id(video_id):
    return dict(videos=mirror.get_utattemita_videos_by_id(video_id))


@app.get("/playlists/{playlist_id}", response_model=Playlist)
def get_playlist_by_id(playlist_id):
    return mirror.get_playlist_by_id(playlist_id)
