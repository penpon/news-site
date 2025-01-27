from fastapi import FastAPI, HTTPException
import feedparser
import aiohttp
import asyncio
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
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


# 単一のRSSフィードを取得し、記事リストを返す関数
async def fetch_feed(session: aiohttp.ClientSession, url: str) -> List[Article]:
    """
    単一のRSSフィードを取得し、記事リストを返す。
    """
    try:
        # 非同期でRSSフィードを取得
        async with session.get(url) as response:
            if response.status != 200:
                # HTTPステータスが200でない場合のエラーログ
                print(f"Failed to fetch {url}: {response.status}")
                return []
            content = await response.text()
            feed = feedparser.parse(content)
            articles = []
            for entry in feed.entries:
                # RSSフィードのエントリを解析してArticleオブジェクトに変換
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
        # RSS取得中の例外をログに出力
        print(f"Error fetching {url}: {e}")
        return []


# 全てのRSSフィードから記事を取得し、統合して返すエンドポイント
@app.get("/api/news", response_model=List[Article])
async def get_news():
    """
    全てのRSSフィードから記事を取得し、統合して返す。
    """
    try:
        # 非同期セッションを作成
        async with aiohttp.ClientSession() as session:
            # 全RSSフィードの非同期タスクを作成
            tasks = [fetch_feed(session, url) for url in RSS_FEEDS]
            # 非同期タスクを並列実行し、逐次処理
            articles = []
            for future in asyncio.as_completed(tasks):
                articles.extend(await future)
            # 重複を排除する（リンクを基準に）
            articles = list({article.link: article for article in articles}.values())
            # 記事を公開日順にソート（公開日が空の場合を考慮）
            articles.sort(
                key=lambda x: datetime.strptime(x.published, "%a, %d %b %Y %H:%M:%S %Z")
                if x.published
                else datetime.min,
                reverse=True,
            )
            return articles
    except Exception as e:
        # エラー発生時にHTTP 500を返す
        raise HTTPException(status_code=500, detail=f"Failed to fetch news: {str(e)}")


# アプリケーションの起動
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", reload=True)
