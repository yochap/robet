import requests
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import time
import warnings
import json
import os

# User-Agent 列表，用于绕过某些网站的反爬虫机制
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
    # 国内新闻源（RSS）
    "https://rss.sina.com.cn/tech/rollnews.xml",
    "https://feeds.bloomberg.com/markets/news/rss.rss",
    
    # 国内科技媒体
    "https://www.toutiao.com/api/search/homepage_feed/",
    "https://www.36kr.com/feed",
    "https://tech.ifeng.com/",
    "https://tech.qq.com/",
    "https://finance.sina.com.cn/",
    "https://stock.eastmoney.com/",
    
    # 芯片/半导体相关
    "https://www.semi.org/news",
    "https://www.eenewseurope.com/",
    "https://www.eetasia.com/feed/",
    "https://www.anandtech.com/rss/",
    "https://www.tomshardware.com/feeds/all",
    "https://www.pcworld.com/index.rss",
    
    # 国际新闻源（允许爬虫的）
    "https://feeds.cnbc.com/nbcnews/public/tech",
    "https://feeds.arstechnica.com/arstechnica/index",
    "https://feeds.engadget.com/webfeeds/rss2.0/",
    
    # 商业新闻
    "https://www.ftchinese.com/rss/news",
    "https://feeds.bloomberg.com/technology.rss",
    "https://www.wsj.com/xml/rss/3_7455.xml",
    
    # 中文财经新闻
    "https://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/zxgg/index.phtml",
    "https://www.yicai.com/rss/news.xml",
    "https://www.caixin.com/rss/index.xml",
    # 新增用户请求的新闻源
    "https://www.10jqka.com.cn/",  # 同花顺
    "http://stock.10jqka.com.cn/",  # 同花顺 - 股票频道
    "https://www.eastmoney.com/",  # 东方财富首页
    "https://finance.eastmoney.com/",  # 东方财富财经频道
    "https://bloombergnew.buzzing.cc/",  # 用户提供的镜像/聚合站点
]

# 从外部配置文件加载 NEWS_URLS（优先）
CONFIG_NEWS_FILE = os.path.join(os.path.dirname(__file__), "news_urls.json")

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

    print("使用内置默认新闻源")
    return DEFAULT_NEWS_URLS

# 最终使用的列表
NEWS_URLS = load_news_urls()

BULL_KEYWORDS = [
    "中国全面豁免",
    "中荷达成",
    "荷兰撤销对 Nexperia ",
    "荷兰法院恢复",
    "支持 Nexperia 正常",
    "Nexperia 恢复",
    "闻泰科技利好",
    "利好闻泰科技",
    "闻泰科技宣布",
    "中国放宽半导体出口",
    "中欧芯片供应链恢复",
    "中欧启动半导体",
    "德国高层访华"
    "荷兰安世"
]

BEAR_KEYWORDS = [
    "中方重新收紧出口",
    "荷兰法院裁定 Nexperia 移",
    "资产冻结",
    "德国或欧盟统一外资审查强化",
    "欧洲车企供应停产"
]

INTERVAL = 300  # 每5分钟抓一次
PUSH_PLUS_SENDKEY = "0428f6ebba1f41e6823e80649dce4cb3"  # 已替换你的SendKey

# 测试模式开关（改为 True 可以快速测试警报）
TEST_MODE = False

# 系统状态
SYSTEM_READY = True  # 系统已验证就绪

# =========================
# 函数区
# =========================
def fetch_news(url, retries=2):
    """
    抓取新闻，支持重试和多种 User-Agent
    """
    import random
    
    for attempt in range(retries):
        try:
            # 随机选择 User-Agent
            headers = HEADERS.copy()
            headers["User-Agent"] = random.choice(USER_AGENTS)
            
            # 添加随机延迟，避免被检测为爬虫
            if attempt > 0:
                time.sleep(random.uniform(1, 3))
            
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            
            # 根据 URL 判断是否为 XML 文件
            if url.endswith(".xml") or "rss" in url.lower():
                soup = BeautifulSoup(resp.text, "xml")
            else:
                soup = BeautifulSoup(resp.text, "html.parser")
            
            # 尝试多种标签来获取标题
            headlines = []
            for tag in ['h3', 'h2', 'h1', 'title', 'item', 'entry', 'article', 'a']:
                elements = soup.find_all(tag)
                headlines.extend([h.get_text().strip() for h in elements])
            
            # 过滤空白标题和去重
            headlines = list(set([h for h in headlines if h and len(h.strip()) > 2]))
            
            if headlines:
                print(f"✓ 成功抓取 {url} ({len(headlines)} 条标题)")
                return headlines
            else:
                print(f"✓ 连接 {url} 成功但无内容")
                return []
                
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 401:
                print(f"⚠️ [{attempt+1}/{retries}] {url}: 需要授权 (401)")
            elif status_code == 403:
                print(f"⚠️ [{attempt+1}/{retries}] {url}: 已被禁止 (403)")
            elif status_code == 404:
                print(f"⚠️ [{attempt+1}/{retries}] {url}: 资源不存在 (404)")
            else:
                print(f"⚠️ [{attempt+1}/{retries}] {url}: HTTP 错误 {status_code}")
        except requests.exceptions.Timeout:
            print(f"⚠️ [{attempt+1}/{retries}] {url}: 超时")
        except requests.exceptions.ConnectionError:
            print(f"⚠️ [{attempt+1}/{retries}] {url}: 连接错误")
        except Exception as e:
            print(f"⚠️ [{attempt+1}/{retries}] {url}: {type(e).__name__} - {str(e)[:80]}")
    
    return []

def check_keywords(headlines, keywords):
    hits = []
    for title in headlines:
        for kw in keywords:
            if kw.lower() in title.lower():
                hits.append((kw, title))
    return hits

def send_pushplus_alert(message):
    url = "http://www.pushplus.plus/send"
    data = {
        "token": PUSH_PLUS_SENDKEY,
        "title": "闻泰科技事件监控",
        "content": message
    }
    try:
        requests.post(url, json=data)
    except Exception as e:
        print(f"PushPlus推送失败: {e}")

# =========================
# 测试函数
# =========================
def test_alert_system():
    """测试警报系统 - 模拟真实警报"""
    print("\n" + "=" * 50)
    print("🧪 进入测试模式")
    print("=" * 50)
    
    # 测试用例 1: 利好消息
    print("\n[测试 1] 发送利好警报...")
    bull_msg = "闻泰利好消息\n关键词: 中国全面豁免 Nexperia 芯片出口管制\n标题: 速报！中国全面豁免 Nexperia 芯片出口管制\n来源: https://rss.sina.com.cn/tech/"
    send_pushplus_alert(bull_msg)
    time.sleep(2)
    
    # 测试用例 2: 利空消息
    print("[测试 2] 发送利空警报...")
    bear_msg = "闻泰利空消息\n关键词: 中方重新收紧出口\n标题: 最新：中方重新收紧芯片出口管制\n来源: https://feeds.bloomberg.com/"
    send_pushplus_alert(bear_msg)
    time.sleep(2)
    
    # 测试用例 3: 连接测试
    print("[测试 3] 测试网络连接...")
    try:
        resp = requests.get("https://www.baidu.com", timeout=5)
        print(f"✅ 网络连接正常 (状态码: {resp.status_code})")
    except Exception as e:
        print(f"❌ 网络连接失败: {e}")
    
    print("\n✅ 测试完成！检查你的手机/邮箱是否收到推送")
    print("=" * 50)

# =========================
# 主循环
# =========================
if __name__ == "__main__":
    import datetime
    print("=" * 50)
    print("🚀 闻泰科技事件实时监控启动")
    print(f"⏰ 启动时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📰 监控 {len(NEWS_URLS)} 个新闻源")
    print(f"⏱️  更新间隔: {INTERVAL} 秒")
    print(f"🧪 测试模式: {'开启' if TEST_MODE else '关闭'}")
    print("=" * 50)
    
    # 如果启用测试模式，先运行测试
    if TEST_MODE:
        test_alert_system()
        exit()
    
    loop_count = 0
    while True:
        loop_count += 1
        print(f"\n🔄 第 {loop_count} 轮抓取 - {datetime.datetime.now().strftime('%H:%M:%S')}")
        
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
                print(f"✅ {msg}")
                send_pushplus_alert(msg)
                alert_count += 1

            for kw, title in bear_hits:
                msg = f"闻泰利空消息\n关键词: {kw}\n标题: {title}\n来源: {url}"
                print(f"❌ {msg}")
                send_pushplus_alert(msg)
                alert_count += 1

        print(f"\n📊 本轮结果: 成功抓取 {success_count} 个源，触发 {alert_count} 个警报")
        print(f"⏳ 等待 {INTERVAL} 秒后下一轮抓取...")
        time.sleep(INTERVAL)
