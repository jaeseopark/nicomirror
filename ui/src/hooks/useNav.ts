import { useNavigate } from "react-router-dom";

export const useNav = () => {
  const navigate = useNavigate();

  return {
    navRoot: () => navigate("/"),
    navDownloads: () => navigate("/downloads"),
    navVideo: (videoId: string) => navigate(`/videos/${videoId}`),
    navPlaylist: (playlistId: string) => navigate(`/playlists/${playlistId}`),
    navSearchResult: (searchId: string) => navigate(`/searches/${searchId}`),
  };
};
