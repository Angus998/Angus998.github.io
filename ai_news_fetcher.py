import os
import feedparser
import requests
from datetime import datetime
from functools import lru_cache
from git import Repo
from pathlib import Path
from bs4 import BeautifulSoup
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# 基础配置
CONFIG = {
    "rss_feeds": [
        'https://www.artificialintelligence-news.com/feed/',
        'https://venturebeat.com/tag/ai/feed/'
    ],
    "output_dir": "news_output",
    # "github_repo": "https://github.com/Angus998/Angus998.github.io.git",  # http格式
    "github_repo": "git@github.com:Angus998/Angus998.github.io.git",  # ssh格式
    "git_branch": "test",
    "max_news": 20  # 最大新闻数量
}

# 初始化目录
Path(CONFIG['output_dir']).mkdir(exist_ok=True)

@lru_cache(maxsize=128)
def parse_rss(feed_url):
    """
    解析 RSS 源，使用 lru_cache 缓存结果以提高性能。
    :param feed_url: RSS 源的 URL
    :return: 解析后的 RSS 数据
    """
    try:
        return feedparser.parse(feed_url)
    except Exception as e:
        logging.error(f"解析 RSS 源 {feed_url} 失败: {e}")
        return None

def fetch_news():
    """
    抓取最新 AI 新闻
    :return: 按发布时间排序的新闻列表
    """
    news_items = []
    for feed_url in CONFIG['rss_feeds']:
        feed = parse_rss(feed_url)
        if feed and feed.entries:
            for entry in feed.entries[:CONFIG['max_news']]:
                try:
                    published = datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d %H:%M')
                    summary = BeautifulSoup(entry.get('summary', ''), 'html.parser').get_text()[:300] + '...'
                    news_items.append({
                        'title': entry.get('title', '无标题'),
                        'link': entry.link,
                        'published': published,
                        'summary': summary
                    })
                except Exception as e:
                    logging.error(f"处理新闻条目失败: {e}")
    return sorted(news_items, key=lambda x: x['published'], reverse=True)

def generate_txt(news_items):
    """
    生成 TXT 文件
    :param news_items: 新闻列表
    :return: 生成的 TXT 文件路径
    """
    filename = os.path.join(CONFIG['output_dir'], f"ai_news_{datetime.now().strftime('%Y%m%d')}.txt")
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"AI热点新闻更新 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n")
            f.write("=" * 60 + "\n\n")
            for idx, item in enumerate(news_items, 1):
                f.write(f"{idx}. {item['title']}\n")
                f.write(f"   时间: {item['published']}\n")
                f.write(f"   链接: {item['link']}\n")
                f.write(f"   摘要: {item['summary']}\n\n")
                f.write("-" * 60 + "\n\n")
        logging.info(f"成功生成 TXT 文件: {filename}")
        return filename
    except Exception as e:
        logging.error(f"生成 TXT 文件失败: {e}")
        return None

def generate_html(news_items):
    """
    生成 HTML 文件
    :param news_items: 新闻列表
    :return: 生成的 HTML 文件路径
    """
    filename = os.path.join(CONFIG['output_dir'], "index.html")
    news_list = []
    for item in news_items:
        news_list.append(f"""
        <div class="news-item p-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold"><a href="{item['link']}" target="_blank">{item['title']}</a></h3>
            <div class="meta text-sm text-gray-500 my-2">
                <span class="time">🕒 {item['published']}</span>
            </div>
            <p class="summary text-gray-700 leading-6">{item['summary']}</p>
        </div>
        """)
    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI新闻聚合 - {datetime.now().strftime('%Y-%m-%d')}</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="container mx-auto p-4">
        <h1 class="text-2xl font-bold mb-4">最新AI新闻</h1>
        <p class="text-gray-600 mb-4">更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        {"".join(news_list)}
    </body>
    </html>
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logging.info(f"成功生成 HTML 文件: {filename}")
        return filename
    except Exception as e:
        logging.error(f"生成 HTML 文件失败: {e}")
        return None


def git_push():
    """
    自动提交到 GitHub
    """
    try:
        # 初始化本地仓库
        repo = Repo.init(os.getcwd())
        # 添加远程仓库地址
        origin = repo.create_remote('origin', CONFIG['github_repo'])
        # 添加文件到暂存区
        repo.git.add(CONFIG['output_dir'])
        # 提交更改
        repo.index.commit(f"自动更新新闻 {datetime.now().strftime('%Y%m%d-%H%M')}")
        # 推送文件到远程仓库
        origin.push(refspec=f'{CONFIG["git_branch"]}:{CONFIG["git_branch"]}')
        logging.info("GitHub 推送成功")
    except Exception as e:
        logging.error(f"Git 操作失败: {e}")


if __name__ == "__main__":
    # logging.info("开始抓取新闻...")
    # news = fetch_news()
    # if news:
    #     logging.info("生成文件中...")
    #     txt_file = generate_txt(news)
    #     html_file = generate_html(news)
    #     if txt_file and html_file:
    #         logging.info("正在上传到 GitHub...")
    #         git_push()
    #         logging.info(f"完成！生成文件：{txt_file} 和 {html_file}")
    # else:
    #     logging.info("未获取到新闻数据")

    # 初始化本地仓库
    repo = Repo.init(os.getcwd())
    # 添加远程仓库地址
    origin = repo.create_remote('origin', CONFIG['github_repo'])
    # 添加文件到暂存区
    repo.git.add(CONFIG['output_dir'])
    # 提交更改
    repo.index.commit(f"自动更新新闻 {datetime.now().strftime('%Y%m%d-%H%M')}")
    # 推送文件到远程仓库
    origin.push(refspec=f'{CONFIG["git_branch"]}:{CONFIG["git_branch"]}')
    logging.info("GitHub 推送成功")
