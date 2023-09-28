import RelativeTime from "@yaireo/relative-time";

const relativeTime = new RelativeTime();
const compactFormatter = Intl.NumberFormat("en", { notation: "compact" });

export const durationToString = (duration: number) => {
  var date = new Date(0);
  date.setSeconds(duration);
  return date.toISOString().substring(14, 19);
};

export const timestampToString = (
  timestamp: number,
): {
  timestamp: number;
  dateString: string;
  relativeString: string;
} => {
  const d = new Date(0);
  d.setUTCSeconds(timestamp);

  const dateString = d.toLocaleDateString();

  return {
    timestamp,
    dateString,
    relativeString: relativeTime.from(d),
  };
};

export const toCompactString = compactFormatter.format;
