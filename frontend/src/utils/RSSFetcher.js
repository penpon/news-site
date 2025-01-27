// src/utils/RSSFetcher.js
import axios from "axios";

const fetchRSS = async (url) => {
  try {
    const response = await axios.get(
      `http://localhost:5000/proxy?url=${encodeURIComponent(url)}`
    );
    const parser = new DOMParser();
    const xml = parser.parseFromString(response.data, "text/xml");
    const items = xml.querySelectorAll("item");
    const articles = Array.from(items).map((item) => ({
      title: item.querySelector("title")?.textContent || "",
      link: item.querySelector("link")?.textContent || "",
      description: item.querySelector("description")?.textContent || "",
      pubDate: item.querySelector("pubDate")?.textContent || "",
    }));
    return articles;
  } catch (error) {
    console.error("Error fetching RSS feed:", error);
    return [];
  }
};

export default fetchRSS;
