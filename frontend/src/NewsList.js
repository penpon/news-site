// src/NewsList.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const NewsList = () => {
    const [articles, setArticles] = useState([]); // 空配列で初期化
    const [loading, setLoading] = useState(true); // ローディング状態
    const [error, setError] = useState(null); // エラーメッセージ

    useEffect(() => {
        const fetchNews = async () => {
            try {
                const response = await axios.get('http://localhost:8010/api/news', {
                    params: {
                        urls: [
                            "https://business.nikkei.com/rss/sns/nb.rdf",
                            "https://www.businessinsider.jp/feed/index.xml",
                            "https://xtech.nikkei.com/rss/xtech-it.rdf",
                            "https://rss.itmedia.co.jp/rss/2.0/aiplus.xml",
                            "https://b.hatena.ne.jp/hotentry/it.rss",
                            "https://b.hatena.ne.jp/q/ai?users=5&mode=rss&sort=recent",
                            "https://zenn.dev/topics/機械学習/feed",
                            "https://zenn.dev/topics/ai/feed",
                            "https://zenn.dev/topics/生成ai/feed",
                            "https://zenn.dev/topics/deeplearning/feed",
                            "https://zenn.dev/topics/llm/feed",
                            "https://zenn.dev/topics/nlp/feed",
                            "https://zenn.dev/topics/python/feed",
                            "https://zenn.dev/topics/googlecloud/feed",
                            "https://cloudblog.withgoogle.com/rss/",
                            "https://cloudblog.withgoogle.com/ja/rss/",
                            "https://blog.g-gen.co.jp/feed",
                            "https://jamesg.blog/2024/05/23/hf-papers-rss/",
                            "https://www.techno-edge.net/rss20/index.rdf",
                        ]
                    }
                });
                console.log("Fetched articles:", response.data); // デバッグログ
                setArticles(response.data); // データ更新
            } catch (err) {
                setError('ニュースの取得に失敗しました。'); // エラー設定
                console.error(err); // デバッグ用エラーログ
            } finally {
                setLoading(false); // ローディング完了
            }
        };
        fetchNews();
    }, []);

    if (loading) return <p>読み込み中...</p>; // ローディング中の表示
    if (error) return <p>{error}</p>; // エラー時の表示

    return (
        <div>
            <h1>最新ニュース</h1>
            <ul>
                {articles.map((article, index) => (
                    <li key={index}>
                        <a href={article.link} target="_blank" rel="noopener noreferrer">
                            {article.title}
                        </a>
                        <p>{article.source}</p>
                        <p>{article.published}</p>
                        <p dangerouslySetInnerHTML={{ __html: article.summary }}></p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default NewsList;

