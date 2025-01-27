import sys
import logging
from fastapi import FastAPI, HTTPException
import feedparser
import aiohttp
import asyncio
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from dateutil.parser import parse  # 日付フォーマットの柔軟性を高めるため
from fastapi import Query
from itertools import chain
from urllib.parse import unquote
from typing import Union
import os

# FastAPIアプリケーションの作成
app = FastAPI()

# ログの設定
logging.basicConfig(
    level=logging.INFO,  # 必要なら DEBUG に変更
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)

logger = logging.getLogger("rss-fetcher")
logger.setLevel(logging.DEBUG)  # 詳細なデバッグログの有効化

# CORS設定
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
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

# 許可されたURLセット
ALLOWED_URLS_SET = {unquote(url) for url in RSS_FEEDS}


class Article(BaseModel):
    title: str
    link: str
    published: str
    summary: str
    source: str


def is_allowed_url(url: str) -> bool:
    """URLが許可リストにあるか確認"""
    return unquote(url) in ALLOWED_URLS_SET


async def fetch_feed(session: aiohttp.ClientSession, url: str) -> List[Article]:
    """RSSフィードを取得し、パースして記事リストを返す"""
    try:
        async with session.get(url) as response:
            if response.status != 200:
                logger.error(f"Failed to fetch {url}: HTTP {response.status}")
                return []
            content = await response.text()
            feed = feedparser.parse(content)

            if not feed.entries:
                logger.warning(f"No entries found in feed: {url}")
                return []

            articles = []
            for entry in feed.entries:
                try:
                    published = entry.get("published", "")
                    parsed_date = parse(published, fuzzy=True) if published else None
                    article = Article(
                        title=entry.get("title", "No Title"),
                        link=entry.get("link", ""),
                        published=parsed_date.isoformat() if parsed_date else "",
                        summary=entry.get("summary", ""),
                        source=feed.feed.get("title", url),
                    )
                    articles.append(article)
                except Exception as e:
                    logger.error(f"Error parsing article from {url}: {e}")
            return articles
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return []


@app.get("/api/news", response_model=List[Article])
async def get_news(
    urls: Union[List[str], None] = Query(default=None, alias="urls"),
    url: Union[str, None] = Query(default=None, alias="url"),
    limit: int = Query(default=5, ge=1, le=100, alias="limit"),  # デフォルトで5件に設定
):
    """
    ニュースAPIエンドポイント
    記事数を5件に制限
    """
    all_urls = urls if urls else [url]
    if not all_urls or any(not u.strip() for u in all_urls):
        raise HTTPException(status_code=400, detail="Invalid URLs provided")

    timeout = aiohttp.ClientTimeout(total=15)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            articles = await asyncio.gather(
                *[fetch_feed(session, url) for url in all_urls]
            )
            flattened = list(chain.from_iterable(articles))

            # 日付順にソート（新しい順）
            flattened.sort(
                key=lambda a: parse(a.published, fuzzy=True)
                if a.published
                else datetime.min,
                reverse=True,
            )

            # 重複排除
            seen = set()
            unique_articles = [
                a for a in flattened if not (a.link in seen or seen.add(a.link))
            ]

            # 記事数を制限
            limited_articles = unique_articles[:limit]
            return limited_articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
