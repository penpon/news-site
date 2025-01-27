// src/NewsList.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const NewsList = () => {
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchNews = async () => {
            try {
                const response = await axios.get('http://localhost:8010/api/news');
                setArticles(response.data);
            } catch (err) {
                setError('ニュースの取得に失敗しました。');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchNews();
    }, []);

    if (loading) return <p>読み込み中...</p>;
    if (error) return <p>{error}</p>;

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
