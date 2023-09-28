import { useEffect, useMemo, useState } from "react";

import VideoListView from "./VideoListView";
import { getPlaylist } from "./api";

const PlaylistView = ({ playlistId }: { playlistId: string }) => {
  const [playlist, setPlaylist] = useState();

  useEffect(() => {
    getPlaylist(playlistId).then(setPlaylist);
  }, [playlistId]);

  const getContent = () => {
    if (!playlist) {
      return <div>Loading...</div>;
    }

    const { videos } = playlist;
    return <VideoListView videos={videos} />;
  };

  return <div className="playlist-view">{getContent()}</div>;
};

export default PlaylistView;
