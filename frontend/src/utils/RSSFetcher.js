// frontend/src/utils/RSSFetcher.js
import axios from "axios";

const fetchRSS = async (urls) => {
  if (!Array.isArray(urls)) {
    urls = [urls];
  }

  try {
    const responses = await Promise.all(
      urls.map(url => 
        axios.get(`http://localhost:8010/api/news?url=${encodeURIComponent(url)}`)
      )
    );

    return responses.flatMap(response => {
      if (!response.data || typeof response.data !== "string") {
        console.error("Invalid response format");
        return [];
      }

      const parser = new DOMParser();
      const xml = parser.parseFromString(response.data, "text/xml");

      if (xml.querySelector("parsererror")) {
        console.error("Error parsing XML:", xml.querySelector("parsererror"));
        return [];
      }

      const items = xml.querySelectorAll("item");
      return Array.from(items).map((item) => ({
        title: item.querySelector("title")?.textContent || "",
        link: item.querySelector("link")?.textContent || "",
        description: item.querySelector("description")?.textContent || "",
        pubDate: item.querySelector("pubDate")?.textContent || "",
      }));
    });
  } catch (error) {
    console.error("Error fetching RSS feeds:", error.message || error);
    return [];
  }
};

export default fetchRSS;
