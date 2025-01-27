# main.py
from fastapi import FastAPI, HTTPException
import feedparser
import aiohttp
import asyncio
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = [
    "http://localhost:3000",  # Reactのデフォルトポート
    # デプロイ先のフロントエンドURLを追加
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RSSフィードのURLリスト
RSS_FEEDS = [
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


class Article(BaseModel):
    title: str
    link: str
    published: str
    summary: str
    source: str


async def fetch_feed(session: aiohttp.ClientSession, url: str) -> List[Article]:
    try:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Failed to fetch {url}: {response.status}")
                return []
            content = await response.text()
            feed = feedparser.parse(content)
            articles = []
            for entry in feed.entries:
                article = Article(
                    title=entry.get("title", "No Title"),
                    link=entry.get("link", ""),
                    published=entry.get("published", ""),
                    summary=entry.get("summary", ""),
                    source=feed.feed.get("title", url),
                )
                articles.append(article)
            return articles
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []


@app.get("/api/news", response_model=List[Article])
async def get_news():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_feed(session, url) for url in RSS_FEEDS]
        results = await asyncio.gather(*tasks)
        # Flatten the list of lists
        articles = [article for sublist in results for article in sublist]
        # ソース別にソート、または日付順にソートするなどの処理が可能
        articles.sort(key=lambda x: x.published, reverse=True)
        return articles
