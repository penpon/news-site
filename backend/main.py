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
import os

app = FastAPI()

# CORS設定
# 環境変数から許可するオリジンを取得
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
    # 日経ビジネス電子版　最新記事
    "https://business.nikkei.com/rss/sns/nb.rdf",
    # Business Insider
    "https://www.businessinsider.jp/feed/index.xml",
    # 日経クロステック　IT（情報技術）
    "https://xtech.nikkei.com/rss/xtech-it.rdf",
    # ITmedia AI＋
    "https://rss.itmedia.co.jp/rss/2.0/aiplus.xml",
    # はてなブックマーク
    "https://b.hatena.ne.jp/hotentry/it.rss",
    "https://b.hatena.ne.jp/q/ai?users=5&mode=rss&sort=recent",
    # Zennブログ
    "https://zenn.dev/topics/機械学習/feed",
    "https://zenn.dev/topics/ai/feed",
    "https://zenn.dev/topics/生成ai/feed",
    "https://zenn.dev/topics/deeplearning/feed",
    "https://zenn.dev/topics/llm/feed",
    "https://zenn.dev/topics/nlp/feed",
    "https://zenn.dev/topics/python/feed",
    "https://zenn.dev/topics/googlecloud/feed",
    # Google Cloud の公式ブログ、Goole Cloud Japanの公式ブログ
    "https://cloudblog.withgoogle.com/rss/",
    "https://cloudblog.withgoogle.com/ja/rss/",
    # 株式会社G-gen様のブログ
    "https://blog.g-gen.co.jp/feed",
    # Hugging Face Daily Papers
    "https://jamesg.blog/2024/05/23/hf-papers-rss/",
    # テクノエッジ：生成AIウィークリー・生成AIクローズアップ
    "https://www.techno-edge.net/rss20/index.rdf",
]


class Article(BaseModel):
    title: str
    link: str
    published: str
    summary: str
    source: str


async def fetch_feed(session: aiohttp.ClientSession, url: str) -> List[Article]:
    """
    単一のRSSフィードを取得し、記事リストを返す。
    """
    try:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Failed to fetch {url}: HTTP {response.status}")
                return []
            content = await response.text()
            feed = feedparser.parse(content)

            # フィードにエントリが存在しない場合のエラー処理を追加
            if not feed.entries:
                print(f"No entries found in feed: {url}")
                return []

            articles = []
            for entry in feed.entries:
                try:
                    # 公開日の日付解析を追加
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
                    print(f"Error parsing article in {url}: {e}")
            return articles
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []


# 全てのRSSフィードから記事を取得し、統合して返すエンドポイント
@app.get("/api/news", response_model=List[Article])
async def get_news(url: str = Query(None, description="RSS feed URL")):
    """
    全てのRSSフィードから記事を取得し、統合して返す。
    """
    # URLバリデーションを追加
    if url is None or not url.strip():
        raise HTTPException(status_code=400, detail="Invalid or missing URL parameter")

    # URLがリストに存在するか検証
    if url not in RSS_FEEDS:
        raise HTTPException(
            status_code=400, detail="URL is not in the allowed RSS_FEEDS list"
        )

    # RSSフィードを取得
    timeout = aiohttp.ClientTimeout(total=10)  # タイムアウト時間を10秒に設定
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            articles = await fetch_feed(session, url)
            # 重複する記事を排除
            articles = list(
                {
                    (article.link, article.title): article for article in articles
                }.values()
            )
            # 日付でソート
            articles.sort(
                key=lambda x: parse(x.published, fuzzy=True)
                if x.published
                else datetime.min,
                reverse=True,
            )
            return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch news: {str(e)}")


# アプリケーションの起動
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", reload=True)
