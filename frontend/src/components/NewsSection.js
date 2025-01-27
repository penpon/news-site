// frontend/src/components/NewsSection.js
import React, { useEffect, useState } from "react";
import fetchRSS from "../utils/RSSFetcher";
import "./NewsSection.css";

const NewsSection = ({ title, feedUrls }) => {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
  const loadArticles = async () => {
    try {
      // フィードごとのデータを取得
      const responses = await Promise.all(feedUrls.map((url) => fetchRSS(url)));

      // 各レスポンスをログに記録
      responses.forEach((response, index) => {
        console.log(`Response for URL ${feedUrls[index]}:`, response);
      });

      // レスポンスから記事を抽出し、統合
      const articles = responses.flatMap((response) => {
        if (Array.isArray(response)) {
          return response; // 配列データを直接返す場合
        }
        console.warn(`Response from URL is missing articles:`, response);
        return [];
      });

      console.log("Combined Articles:", articles);
      setArticles(articles);
    } catch (error) {
      console.error("Error loading articles:", error);
    }
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

