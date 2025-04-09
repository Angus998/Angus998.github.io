import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 常见科技新闻源的 RSS 订阅地址（需要根据实际情况调整）
RSS_FEEDS = [
    # 'http://fetchrss.com/rss/66048c984e9c8f3a4b8b456766048c8b458b4567a58d3c6.atom',
    'https://www.artificialintelligence-news.com/feed/',
    'https://venturebeat.com/tag/ai/feed/',
    'https://www.technologyreview.com/topic/artificial-intelligence/feed/'
]

# 保存文件名
FILENAME = 'ai_news.txt'


def is_recent(published_time):
    """
    检查新闻是否是最近 24 小时内发布的
    """
    return datetime(*published_time[:6]) > datetime.now() - timedelta(hours=24)


def get_ai_news_rss():
    """
    从 RSS 源获取最近 24 小时内的 AI 新闻
    """
    news_items = []
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                if 'published_parsed' in entry and is_recent(entry.published_parsed):
                    summary = BeautifulSoup(entry.get('summary', ''), 'html.parser').get_text()[:200] + '...'
                    news_items.append({
                        'title': entry.title,
                        'link': entry.link,
                        'published': entry.published,
                        'summary': summary
                    })
        except requests.RequestException as e:
            logging.error(f"网络请求错误，解析 {feed_url} 时出错: {str(e)}")
        except Exception as e:
            logging.error(f"解析 {feed_url} 时发生未知错误: {str(e)}")
    return sorted(news_items, key=lambda x: x['published'], reverse=True)


def save_to_txt(news_items, filename=FILENAME):
    """
    将新闻条目保存到文本文件中
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Latest AI News ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")
            f.write("=" * 50 + "\n\n")
            for idx, item in enumerate(news_items, 1):
                f.write(f"{idx}. {item['title']}\n")
                f.write(f"   Published: {item['published']}\n")
                f.write(f"   Link: {item['link']}\n")
                f.write(f"   Summary: {item['summary']}\n\n")
                f.write("-" * 50 + "\n\n")
        logging.info(f"成功保存 {len(news_items)} 条资讯到 {filename}")
    except Exception as e:
        logging.error(f"保存文件时出错: {str(e)}")


if __name__ == "__main__":
    logging.info("正在抓取 AI 热点资讯...")
    news = get_ai_news_rss()
    if news:
        save_to_txt(news)
    else:
        logging.info("未能获取到最新资讯")
