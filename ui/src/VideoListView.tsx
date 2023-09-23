import VideoCardView from "./VideoCardView";

const ViewListView = ({ videos }: { videos: object[] }) => {
  return (
    <div>
      {videos.map((video) => (
        <VideoCardView video={video} />
      ))}
    </div>
  );
};

export default ViewListView;
