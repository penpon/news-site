// src/App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import NewsSection from "./components/NewsSection";
import "./index.css";

const App = () => {
  return (
    <Router>
      <div className="container">
        <Sidebar />
        <div className="main-content">
          <Routes>
            <Route
              path="/"
              element={
                <>
                  <NewsSection
                    title="日経ビジネス"
                    feedUrl="https://business.nikkei.com/rss/sns/nb.rdf"
                  />
                  <NewsSection
                    title="Business Insider"
                    feedUrl="https://www.businessinsider.jp/feed/index.xml"
                  />
                  <NewsSection
                    title="日経クロステック"
                    feedUrl="https://xtech.nikkei.com/rss/xtech-it.rdf"
                  />
                  <NewsSection
                    title="ITmedia AI＋"
                    feedUrl="https://rss.itmedia.co.jp/rss/2.0/aiplus.xml"
                  />
                  <NewsSection
                    title="はてなブックマーク"
                    feedUrls={[
                      "https://b.hatena.ne.jp/q/ai?users=5&mode=rss&sort=recent",
                      "https://b.hatena.ne.jp/hotentry/it.rss",
                    ]}
                  />
                  <NewsSection
                    title="Zennブログ"
                    feedUrls={[
                      "https://zenn.dev/topics/機械学習/feed",
                      "https://zenn.dev/topics/ai/feed",
                      "https://zenn.dev/topics/生成ai/feed",
                      "https://zenn.dev/topics/deeplearning/feed",
                      "https://zenn.dev/topics/llm/feed",
                      "https://zenn.dev/topics/nlp/feed",
                      "https://zenn.dev/topics/python/feed",
                      "https://zenn.dev/topics/googlecloud/feed",
                    ]}
                  />
                </>
              }
            />
            <Route path="/articles" element={<h1>新着記事一覧</h1>} />
            <Route path="/papers" element={<h1>新着論文一覧</h1>} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;

