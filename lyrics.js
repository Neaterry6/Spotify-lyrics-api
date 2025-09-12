const { getLyrics } = require("genius-lyrics-api");

const options = {
  apiKey: "v7yS4P9onNcPHtb8MKEWcnooMIDxLKGZwnbKe1BbSuvJIth_9IEWSRDOkj51lser",
  title: process.argv[2],
  artist: process.argv[3],
  optimizeQuery: true
};

getLyrics(options).then((lyrics) => {
  console.log(lyrics || "Lyrics not found.");
});
