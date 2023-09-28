export type Classification = {
  input: string;
} & (
  | {
      sanitized: string;
      type: "video" | "playlist";
    }
  | { type: "unknown" }
);

const VIDEO_REGEX = /sm[0-9]+|nm[0-9]+/;
const PLAYLIST_REGEX = /mylist\/[0-9]+/;

const sanitizePlaylistId = (original: string) => original.split("/").pop()!;

export const classifySearchTerm = (input: string): Classification => {
  let match = input.match(VIDEO_REGEX);
  if (match) {
    return { input, type: "video", sanitized: match[0] };
  }

  match = input.match(PLAYLIST_REGEX);
  if (match) {
    return { input, type: "playlist", sanitized: sanitizePlaylistId(match[0]) };
  }

  return { input, type: "unknown" };
};

export const tokenize = (input: string): Classification[] => {
  throw new Error("not implemented");
};
