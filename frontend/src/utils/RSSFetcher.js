// frontend/src/utils/RSSFetcher.js
import axios from "axios";

const fetchRSS = async (urls) => {
  if (!Array.isArray(urls)) {
    urls = [urls];
  }

  try {
    const responses = await Promise.all(
      urls.map((url) =>
        axios.get(`http://localhost:8010/api/news?url=${encodeURIComponent(url)}`)
      )
    );

    return responses.flatMap((response) => {
      if (response.data) {
        return response.data; // 必要に応じて `response.data.articles` を確認
      } else {
        console.error("Invalid response format:", response);
        return [];
      }
    });
  } catch (error) {
    console.error("Error fetching RSS feeds:", error.message || error);
    return [];
  }
};

export default fetchRSS;

