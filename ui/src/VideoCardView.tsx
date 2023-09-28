import { HStack, Heading, Tag } from "@chakra-ui/react";
import { Link as ChakraLink } from "@chakra-ui/react";
import { Link as ReactRouterLink } from "react-router-dom";
import styled from "styled-components";

import { durationToString, timestampToString, toCompactString } from "./utils/number";

const StyledVideoCardDiv = styled.div`
  border: 1px solid rgba(21, 21, 21, 0.35);
  border-radius: 15px;
  padding: 1em;
`;

const VideoCardView = ({ video, enableHyperlink }: { video: any; enableHyperlink?: boolean }) => {
  const { title, thumbnail_url: thumbnailUrl, timestamp, views, likes, id: videoId, duration, parent_video_id: parentVideoId } = video;
  const t = timestampToString(timestamp);
  const likesRatio = likes / views;

  const getContent = () => (
    <StyledVideoCardDiv>
      <HStack>
        <div className="video-thumbnail">
          <img src={thumbnailUrl} />
        </div>
        <div className="video-metadata">
          {parentVideoId && <Tag>Cover</Tag>}
          <Heading size="md">{title}</Heading>
          <div className="video-timestamp">
            <label>
              {t.dateString} ({t.relativeString})
            </label>
          </div>
          <div className="video-counts">
            <Tag>{toCompactString(views)}</Tag>
            <Tag>{(likesRatio * 100).toFixed(0)}%</Tag>
            <Tag>{durationToString(duration)}</Tag>
          </div>
        </div>
      </HStack>
    </StyledVideoCardDiv>
  );

  if (enableHyperlink) {
    return (
      <ChakraLink as={ReactRouterLink} to={`/videos/${videoId}`}>
        {getContent()}
      </ChakraLink>
    );
  }
  return getContent();
};

export default VideoCardView;
