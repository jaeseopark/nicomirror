import { SimpleGrid } from "@chakra-ui/react";

import VideoCardView from "./VideoCardView";

const ViewListView = ({ videos }: { videos: object[] }) => {
  // TODO: sort option dropdown
  // TODO: display options (ex. # of columns)

  if (videos.length === 0) {
    return <div>No data</div>
  }

  return (
    <SimpleGrid columns={2} spacing={10}>
      {videos.map((video: any) => (
        <VideoCardView key={video.id} video={video} enableHyperlink />
      ))}
    </SimpleGrid>
  );
};

export default ViewListView;
