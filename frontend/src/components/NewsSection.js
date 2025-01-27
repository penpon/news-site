// frontend/src/components/NewsSection.js
// frontend/src/components/NewsSection.js
import React, { useEffect, useState } from "react";
import fetchRSS from "../utils/RSSFetcher";
import "./NewsSection.css";

const NewsSection = ({ title, feedUrls = [] }) => {
  // ジャンルごとの記事を保持
  const [categorizedArticles, setCategorizedArticles] = useState({});

  useEffect(() => {
    const loadArticles = async () => {
      try {
        // feedUrls のバリデーション
        if (!feedUrls || !Array.isArray(feedUrls) || feedUrls.length === 0) {
          console.error("Invalid feed URLs:", feedUrls); // 詳細なログ
          return;
        }

        // API呼び出しとエラーハンドリング
        const responses = await Promise.all(
          feedUrls.map((url) =>
            fetchRSS(url).catch((err) => {
              console.error(`Error fetching URL: ${url}`, err);
              return []; // エラー時は空配列を返す
            })
          )
        );

        // URL をカテゴリ名にマッピング
        const urlToCategory = {
          "https://business.nikkei.com/rss/sns/nb.rdf": "日経ビジネス",
          "https://www.businessinsider.jp/feed/index.xml": "Business Insider",
          "https://xtech.nikkei.com/rss/xtech-it.rdf": "日経クロステック IT",
          "https://rss.itmedia.co.jp/rss/2.0/aiplus.xml": "ITmedia AI＋",
          "https://b.hatena.ne.jp/hotentry/it.rss": "はてなブックマーク - 人気エントリー",
          "https://b.hatena.ne.jp/q/ai?users=5&mode=rss&sort=recent": "はてなブックマーク - AIクエリ",
          "https://zenn.dev/topics/機械学習/feed": "Zenn - 機械学習",
          "https://zenn.dev/topics/ai/feed": "Zenn - AI",
          "https://zenn.dev/topics/生成ai/feed": "Zenn - 生成AI",
          "https://zenn.dev/topics/deeplearning/feed": "Zenn - ディープラーニング",
          "https://zenn.dev/topics/llm/feed": "Zenn - LLM",
          "https://zenn.dev/topics/nlp/feed": "Zenn - NLP",
          "https://zenn.dev/topics/python/feed": "Zenn - Python",
          "https://zenn.dev/topics/googlecloud/feed": "Zenn - Google Cloud",
          "https://cloudblog.withgoogle.com/rss/": "Google Cloud - 英語公式",
          "https://cloudblog.withgoogle.com/ja/rss/": "Google Cloud - 日本語公式",
          "https://blog.g-gen.co.jp/feed": "G-gen Blog",
          "https://jamesg.blog/2024/05/23/hf-papers-rss/": "Hugging Face Daily Papers",
          "https://www.techno-edge.net/rss20/index.rdf": "テクノエッジ - 生成AIウィークリー",
        };

        // レスポンスをカテゴリごとに整理
        const categorized = {};
        responses.forEach((response, index) => {
          const category = urlToCategory[feedUrls[index]] || "その他";
          if (!categorized[category]) {
            categorized[category] = [];
          }
          if (Array.isArray(response)) {
            categorized[category].push(...response);
          } else {
            console.warn(
              `Response from URL is missing articles: ${feedUrls[index]}`,
              response
            );
          }
        });

        // ログ出力
        console.log("Categorized Articles:", categorized);

        // 状態を更新
        setCategorizedArticles(categorized);
      } catch (error) {
        console.error("Error loading articles:", error);
      }
    };

    loadArticles();
  }, [feedUrls]);

  return (
    <div className="news-section">
      <h2>{title}</h2>
      {Object.keys(categorizedArticles).map((category) => (
        <div key={category} className="category-section">
          <h3>{category}</h3>
          <div className="articles">
            {categorizedArticles[category].map((article, index) => (
              <div key={index} className="article-card">
                <h4>
                  <a href={article.link} target="_blank" rel="noopener noreferrer">
                    {article.title}
                  </a>
                </h4>
                <p>{article.description}</p>
                <small>
                  {article.pubDate
                    ? new Date(article.pubDate).toLocaleString()
                    : "Invalid Date"}
                </small>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default NewsSection;
