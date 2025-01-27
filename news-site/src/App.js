// App.js
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import "./index.css";

const App = () => {
  return (
    <Router>
      <div className="container">
        {/* サイドバー */}
        <Sidebar />

        {/* メインコンテンツ */}
        <div className="main-content">
          <Routes>
            <Route path="/" element={<h1>ホーム</h1>} />
            <Route path="/articles" element={<h1>新着記事一覧</h1>} />
            <Route path="/papers" element={<h1>新着論文一覧</h1>} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
