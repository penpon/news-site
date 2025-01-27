// frontend/src/components/NewsSection.js

import React, { useEffect, useState } from "react";
import fetchRSS from "../utils/RSSFetcher";
import "./NewsSection.css";

const NewsSection = ({ title, feedUrls }) => {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    const loadArticles = async () => {
      const data = await Promise.all(
        feedUrls.map(url => fetchRSS(url))
      );
      setArticles(data.flat());
    };
    loadArticles();
  }, [feedUrls]);

  return (
    <div className="news-section">
      <h2>{title}</h2>
      <div className="articles">
        {articles.map((article, index) => (
          <div key={index} className="article-card">
            <h3>
              <a href={article.link} target="_blank" rel="noopener noreferrer">
                {article.title}
              </a>
            </h3>
            <p>{article.description}</p>
            <small>{new Date(article.pubDate).toLocaleString()}</small>
          </div>
        ))}
      </div>
    </div>
  );
};

export default NewsSection;
