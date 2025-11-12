#!/usr/bin/env python3
# monitor.py

import requests
from bs4 import BeautifulSoup
import time
import json
import os
import random
import datetime

# ========== 配置 ==========
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
]

HEADERS = {
    "User-Agent": USER_AGENTS[0],
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://www.google.com/",
}

DEFAULT_NEWS_URLS = [
    "https://rss.sina.com.cn/tech/rollnews.xml",
    "https://feeds.bloomberg.com/markets/news/rss.rss",
    "https://www.36kr.com/feed",
    "https://tech.ifeng.com/",
    "https://tech.qq.com/",
    "https://finance.sina.com.cn/",
    "https://stock.eastmoney.com/",
    "https://www.semi.org/news",
    "https://www.eenewseurope.com/",
    "https://www.eetasia.com/feed/",
    "https://www.anandtech.com/rss/",
    "https://www.tomshardware.com/feeds/all",
    "https://www.pcworld.com/index.rss",
    "https://feeds.cnbc.com/nbcnews/public/tech",
    "https://feeds.arstechnica.com/arstechnica/index",
    "https://feeds.engadget.com/webfeeds/rss2.0/",
    "https://www.ftchinese.com/rss/news",
    "https://feeds.bloomberg.com/technology.rss",
    "https://www.wsj.com/xml/rss/3_7455.xml",
    "https://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/zxgg/index.phtml",
    "https://www.yicai.com/rss/news.xml",
    "https://www.caixin.com/rss/index.xml",
    "https://www.10jqka.com.cn/",
    "http://stock.10jqka.com.cn/",
    "https://www.eastmoney.com/",
    "https://finance.eastmoney.com/",
    "https://bloombergnew.buzzing.cc/",
]

# external config (可选)
CONFIG_NEWS_FILE = os.path.join(os.path.dirname(__file__), "news_urls.json")

# KEYWORDS
BULL_KEYWORDS = [
    "中国全面豁免", "中荷达成", "荷兰撤销对 Nexperia", "荷兰法院恢复",
    "支持 Nexperia 正常", "Nexperia 恢复", "闻泰科技利好", "利好闻泰科技",
    "闻泰科技宣布", "中国放宽半导体出口", "中欧芯片供应链恢复", "中欧启动半导体",
    "德国高层访华", "荷兰安世"
]
BEAR_KEYWORDS = [
    "中方重新收紧出口", "荷兰法院裁定 Nexperia 移", "资产冻结",
    "德国或欧盟统一外资审查强化", "欧洲车企供应停产"
]

# 默认每次运行是单轮抓取；如果你想更频繁用 Actions 的 cron 调整频率
INTERVAL = 300  # 原脚本中的间隔（保留做日志用）

# 从环境变量读取 PushPlus token（优先）
PUSH_PLUS_SENDKEY = os.getenv("PUSHPLUS_TOKEN", "").strip()

TEST_MODE = False

# =========================
def load_news_urls():
    try:
        if os.path.exists(CONFIG_NEWS_FILE):
            with open(CONFIG_NEWS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and data:
                    print(f"Loaded {len(data)} news sources from {CONFIG_NEWS_FILE}")
                    return data
                else:
                    print(f"配置文件 {CONFIG_NEWS_FILE} 无效，使用默认新闻源")
    except Exception as e:
        print(f"无法加载新闻源配置 {CONFIG_NEWS_FILE}: {e}")
    return DEFAULT_NEWS_URLS

NEWS_URLS = load_news_urls()

def fetch_news(url, retries=2):
    for attempt in range(retries):
        try:
            headers = HEADERS.copy()
            headers["User-Agent"] = random.choice(USER_AGENTS)
            if attempt > 0:
                time.sleep(random.uniform(1, 3))
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            text = resp.text
            if url.endswith(".xml") or "rss" in url.lower():
                soup = BeautifulSoup(text, "xml")
            else:
                soup = BeautifulSoup(text, "html.parser")
            headlines = []
            for tag in ['h3', 'h2', 'h1', 'title', 'item', 'entry', 'article', 'a']:
                elements = soup.find_all(tag)
                for h in elements:
                    t = h.get_text().strip()
                    if t and len(t) > 2:
                        headlines.append(t)
            # 去重
            headlines = list(dict.fromkeys(headlines))
            if headlines:
                print(f"✓ 成功抓取 {url} ({len(headlines)} 条标题)")
                return headlines
            else:
                print(f"✓ 连接 {url} 成功但无内容")
                return []
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else None
            print(f"⚠️ [{attempt+1}/{retries}] {url}: HTTP 错误 {status_code}")
        except requests.exceptions.Timeout:
            print(f"⚠️ [{attempt+1}/{retries}] {url}: 超时")
        except requests.exceptions.ConnectionError:
            print(f"⚠️ [{attempt+1}/{retries}] {url}: 连接错误")
        except Exception as e:
            print(f"⚠️ [{attempt+1}/{retries}] {url}: {type(e).__name__} - {str(e)[:120]}")
    return []

def check_keywords(headlines, keywords):
    hits = []
    for title in headlines:
        for kw in keywords:
            if kw.lower() in title.lower():
                hits.append((kw, title))
    return hits

def send_pushplus_alert(message):
    if not PUSH_PLUS_SENDKEY:
        print("⚠️ 未设置 PUSHPLUS_TOKEN，跳过推送：", message[:200])
        return
    url = "http://www.pushplus.plus/send"
    data = {
        "token": PUSH_PLUS_SENDKEY,
        "title": "闻泰科技事件监控",
        "content": message
    }
    try:
        resp = requests.post(url, json=data, timeout=10)
        if resp.status_code == 200:
            print("→ PushPlus 推送成功")
        else:
            print("→ PushPlus 返回", resp.status_code, resp.text[:200])
    except Exception as e:
        print(f"PushPlus推送失败: {e}")

def main_once():
    start = datetime.datetime.now()
    print("=" * 60)
    print("单次抓取启动:", start.strftime("%Y-%m-%d %H:%M:%S"))
    success_count = 0
    alert_count = 0
    for url in NEWS_URLS:
        headlines = fetch_news(url)
        if not headlines:
            continue
        success_count += 1
        bull_hits = check_keywords(headlines, BULL_KEYWORDS)
        bear_hits = check_keywords(headlines, BEAR_KEYWORDS)
        for kw, title in bull_hits:
            msg = f"闻泰利好消息\n关键词: {kw}\n标题: {title}\n来源: {url}"
            print("✅", msg)
            send_pushplus_alert(msg)
            alert_count += 1
        for kw, title in bear_hits:
            msg = f"闻泰利空消息\n关键词: {kw}\n标题: {title}\n来源: {url}"
            print("❌", msg)
            send_pushplus_alert(msg)
            alert_count += 1
    end = datetime.datetime.now()
    print(f"本次抓取完成：抓取源 {success_count}，触发警报 {alert_count}，耗时 {(end-start).total_seconds():.1f}s")
    print("=" * 60)

if __name__ == "__main__":
    if TEST_MODE:
        # 保留你原来测试函数的逻辑或直接调用 main_once 多次快速模拟
        print("⚠️ TEST_MODE 已开启（请在生产环境关闭）")
    main_once()
