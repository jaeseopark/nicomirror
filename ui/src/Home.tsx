import { useState, useEffect } from "react";
import { getRecentVideos } from "./api";

const Home = () => {
  const [videos, setVideos] = useState<object[]>([]);

  useEffect(() => {
    getRecentVideos().then(setVideos);
  }, []);

  {
    videos.map((video: any) => <div>{video.id}</div>);
  }

  return <div>Home</div>;
};

export default Home;
