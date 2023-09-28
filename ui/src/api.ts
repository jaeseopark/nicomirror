export const getRecentVideos = () => {
  return fetch("/api/videos")
    .then((r) => r.json())
    .then(({ videos }) => videos as object[]);
};

export const getCoverSongs = (videoId: string): Promise<object[]> => {
  return fetch(`/api/videos/${videoId}/utattemita`)
    .then((r) => r.json())
    .then(({ videos }) => videos);
};

export const getVideo = (videoId: string) => {
  return fetch(`/api/videos/${videoId}`).then((r) => r.json());
};

export const getVideoForceFetch = (videoId: String) => {
  return fetch(`/api/videos/${videoId}?force_fetch=true`).then((r) => r.json());
};

export const getPlaylist = (playlistId: string) => {
  return fetch(`/api/playlists/${playlistId}`).then((r) => r.json());
};

export const assignParent = (videoId: string, parentVideoId: string) => {
  return fetch(`/api/videos/${videoId}/parent/${parentVideoId}`, {
    method: "PATCH",
  });
};
