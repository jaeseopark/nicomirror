import { Box, Button } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { HighlightMenu, MenuButton } from "react-highlight-menu";

import VideoCardView from "./VideoCardView";
import { assignParent, getCoverSongs, getVideo, getVideoForceFetch } from "./api";
import { useCache } from "./hooks/useCache";
import { useNav } from "./hooks/useNav";

const VideoView = ({ videoId }: { videoId: string }): JSX.Element => {
  const [video, setVideo] = useState();

  const { navVideo, navSearchResult } = useNav();
  const { setVideosBySearchId } = useCache();

  useEffect(() => {
    getVideo(videoId).then(setVideo);
  }, [videoId]);

  const getContent = () => {
    if (!video) {
      return <label>Loading...</label>;
    }

    const { description, parent_video_id: parentVideoId } = video;

    const getActionItems = () => {
      const items = [];
      if  (parentVideoId)  {
        items.push({
          name: "Go to parent",
          handler: () => {
            navVideo(parentVideoId);
          }
        })
      } else{
        items.push({
          name: "Search cover songs",
          handler: () => {
            const searchId = `${videoId}-cover`;
            getCoverSongs(videoId).then((videos) => setVideosBySearchId(searchId, videos));
            navSearchResult(searchId);
          },
        });
      }
      return items;
    };

    return (
      <Box className="content">
        <VideoCardView video={video} />
        <div className="description-container">
          <label className="description">{description}</label>
          <HighlightMenu
            target=".description"
            allowedPlacements={["top", "bottom"]}
            menu={({ selectedText = "", setClipboard, setMenuOpen }) => (
              <>
                <MenuButton
                  title="Copy to clipboard"
                  icon="clipboard"
                  onClick={() =>
                    setClipboard(selectedText, () => {
                      alert("Copied to clipboard");
                    })
                  }
                />

                <MenuButton
                  title="Search Google"
                  onClick={() => {
                    window.open(`https://www.google.com/search?q=${encodeURIComponent(selectedText)}`);
                  }}
                  icon="magnifying-glass"
                />
                <MenuButton title="Close menu" onClick={() => setMenuOpen(false)} icon="x-mark" />
                <MenuButton title="Set as Parent" onClick={() => assignParent(videoId, selectedText)} icon="LinkIcon" />
              </>
            )}
          />
        </div>
        <div className="actions">
          <Button onClick={() => getVideoForceFetch(videoId).then(setVideo)}>Refresh</Button>
          {getActionItems().map(({ name, handler }) => {
            return (
              <Button key={name} onClick={handler}>
                {name}
              </Button>
            );
          })}
        </div>
      </Box>
    );
  };

  return <div className="video-view">{getContent()}</div>;
};

export default VideoView;
