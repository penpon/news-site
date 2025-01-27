// src/components/RSSFeed.js
import React, { useEffect, useState } from "react";
import fetchRSS from "../utils/RSSFetcher";

const RSSFeed = ({ feedUrl }) => {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const data = await fetchRSS(feedUrl);
      setArticles(data);
    };

    fetchData();
  }, [feedUrl]);

  return (
    <ul>
      {articles.map((article, index) => (
        <li key={index}>
          <a
            href={article.link}
            className={window.location.href === article.link ? "active" : ""}
          >
            {article.title}
          </a>
        </li>
      ))}
    </ul>
  );
};

export default RSSFeed;
