export const getRecentVideos = () => {
  return fetch("/api/videos")
    .then((r) => r.json())
    .then(({ videos }) => videos as object[]);
};

export const getVideo = (videoId: string) => {
  return fetch(`/api/videos/${videoId}`).then((r) => r.json());
};
