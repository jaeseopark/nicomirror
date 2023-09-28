import { useEffect, useState } from "react";

import VideoListView from "./VideoListView";
import { getRecentVideos } from "./api";

const Home = () => {
  const [videos, setVideos] = useState<object[]>([]);

  useEffect(() => {
    getRecentVideos().then(setVideos);
  }, []);

  return (
    <div>
      <VideoListView videos={videos} />
    </div>
  );
};

export default Home;
