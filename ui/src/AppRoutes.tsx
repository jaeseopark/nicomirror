import { Navigate, Route, Routes, useParams } from "react-router-dom";
import App from "./App";
import Home from "./Home";
import VideoView from "./VideoView";
import PlaylistView from "./PlaylistView";

const ParameterizedVideoView = () => {
  const params = useParams();
  return (
    <App>
      <VideoView videoId={params.videoid as string} />
    </App>
  );
};

const ParameterizedPlaylistView = () => {
  const params = useParams();
  return (
    <App>
      <PlaylistView playlistId={params.playlistid as string} />
    </App>
  );
};

const AppRoutes = () => (
  <Routes>
    <Route path="*" element={<Navigate to="/" replace />} />
    <Route
      path="/"
      element={
        <App>
          <Home />
        </App>
      }
    />
    <Route path="/videos/:videoid" element={<ParameterizedVideoView />} />
    <Route path="/playlists/:playlistid" element={<ParameterizedPlaylistView />} />
  </Routes>
);

export default AppRoutes;
