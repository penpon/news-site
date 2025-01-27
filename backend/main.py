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

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,  # 必要なら DEBUG に変更
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,  # 標準出力に明示的に出力
)


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


# ログ設定を追加
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("uvicorn")  # uvicornロガーを使用
logger.setLevel(logging.DEBUG)  # 必要なら DEBUG

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


# 許可リストを事前処理
ALLOWED_URLS_SET = {unquote(url) for url in RSS_FEEDS}


def is_allowed_url(url):
    return unquote(url) in ALLOWED_URLS_SET


def sort_key(article):
    try:
        return parse(article.published, fuzzy=True)
    except:
        return datetime.min


@app.get("/api/news", response_model=List[Article])
async def get_news(
    urls: Union[List[str], None] = Query(default=None, alias="urls"),
    url: Union[str, None] = Query(default=None, alias="url"),
):
    # クエリパラメータを統合
    all_urls: List[str] = urls if urls else [url]

    if not all_urls or any(not u.strip() for u in all_urls):
        logger.error("Invalid URLs provided")
        raise HTTPException(status_code=400, detail="Invalid URLs provided")

    logger.info(f"Received URLs: {all_urls}")

    for url in all_urls:
        # URL詳細ログ
        logger.info(f"Processing URL: {unquote(url)}")
        logger.debug(f"Allowed URLs: {[unquote(u) for u in RSS_FEEDS]}")
        logger.debug(f"Match result: {is_allowed_url(url)}")

        if not is_allowed_url(url):
            logger.warning(f"URL not allowed: {unquote(url)}")
            raise HTTPException(
                status_code=400,
                detail=f"URL {unquote(url)} is not in the allowed RSS_FEEDS list",
            )

    # フィード取得開始ログ
    logger.info("Starting feed fetching process")

    timeout = aiohttp.ClientTimeout(total=15)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            articles = await asyncio.gather(
                *[fetch_feed(session, url) for url in all_urls]
            )
            logger.info(f"Successfully fetched {len(articles)} feeds")

            flattened = list(chain.from_iterable(articles))
            logger.debug(f"Total articles before deduplication: {len(flattened)}")

            # 日付ソート
            flattened.sort(key=sort_key, reverse=True)
            logger.debug("Articles sorted by date")

            # 重複排除
            seen = set()
            result = [a for a in flattened if not (a.link in seen or seen.add(a.link))]
            logger.info(f"Returning {len(result)} unique articles")

            return result

    except Exception as e:
        logger.error(f"Error fetching news: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# アプリケーションの起動
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", reload=True)
