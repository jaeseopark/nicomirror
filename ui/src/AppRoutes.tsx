import { Navigate, Route, Routes, useParams } from "react-router-dom";
import App from "./App";
import Home from "./Home";
import VideoView from "./VideoView";
import PlaylistView from "./PlaylistView";
import DownloadsView from "./DownloadsView";
import VideoListView from "./VideoListView";
import { useCache } from "./hooks/useCache";

const withTopNav = (InnerComponent: (props: any) => JSX.Element) => (props: any) => (
  <App>
    <InnerComponent {...props} />
  </App>
);

const HomeWithNav = withTopNav(Home);
const DownloadsWithNav = withTopNav(DownloadsView);
const VideoWithNav = withTopNav(VideoView);
const PlaylistWithNav = withTopNav(PlaylistView);
const SearchWithNav = withTopNav(VideoListView);

const ParameterizedVideoView = () => {
  const params = useParams();
  return <VideoWithNav videoId={params.videoid as string} />;
};

const ParameterizedPlaylistView = () => {
  const params = useParams();
  return <PlaylistWithNav playlistId={params.playlistid as string} />;
};

const ParameterizedSearchView = () => {
  const params = useParams();
  const { getVideosBySearchId } = useCache();
  const videos = getVideosBySearchId(params.searchId || "");

  return <SearchWithNav videos={videos} />;
};

const AppRoutes = () => (
  <Routes>
    <Route path="*" element={<Navigate to="/" replace />} />
    <Route path="/" element={<HomeWithNav />} />
    <Route path="/downloads" element={<DownloadsWithNav />} />
    <Route path="/videos/:videoid" element={<ParameterizedVideoView />} />
    <Route path="/playlists/:playlistid" element={<ParameterizedPlaylistView />} />
    <Route path="/searches/:searchId" element={<ParameterizedSearchView />} />
  </Routes>
);

export default AppRoutes;
