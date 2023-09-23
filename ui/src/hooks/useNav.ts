import { useNavigate } from "react-router-dom";

const sanitizePlaylistId = (original: string) => original.split("/").slice(-1);

export const useNav = () => {
  const navigate = useNavigate();

  return {
    navRoot: () => navigate("/"),
    navDownloads: () => navigate("/downloads"),
    navVideo: (videoId: string) => navigate(`/videos/${videoId}`),
    navPlaylist: (playlistId: string) => navigate(`/playlists/${sanitizePlaylistId(playlistId)}`),
    navSearchResult: (searchId: string) => navigate(`/searches/${searchId}`),
  };
};
