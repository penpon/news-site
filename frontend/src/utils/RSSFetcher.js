import axios from "axios";

const fetchRSS = async (url) => {
    // URLが未定義または空の場合のハンドリング
  if (!url || typeof url !== "string" || url.trim() === "") {
    console.error("Invalid URL:", url);
    return [];
  }
  try {
    const response = await axios.get(
      `http://localhost:8010/api/news?url=${encodeURIComponent(url)}`
    );

    // Ensure valid XML response
    if (!response.data || typeof response.data !== "string") {
      console.error("Invalid response format");
      return [];
    }

    const parser = new DOMParser();
    const xml = parser.parseFromString(response.data, "text/xml");

    // Handle XML parsing errors
    if (xml.querySelector("parsererror")) {
      console.error("Error parsing XML:", xml.querySelector("parsererror"));
      return [];
    }

    const items = xml.querySelectorAll("item");
    const articles = Array.from(items).map((item) => ({
      title: item.querySelector("title")?.textContent || "",
      link: item.querySelector("link")?.textContent || "",
      description: item.querySelector("description")?.textContent || "",
      pubDate: item.querySelector("pubDate")?.textContent || "",
    }));

    return articles;
  } catch (error) {
    console.error("Error fetching RSS feed:", error.message || error);
    return [];
  }
};

export default fetchRSS;

