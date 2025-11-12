"""
警报测试脚本 - 无需等待真实新闻，快速测试警报功能
"""
import requests
import time

PUSH_PLUS_SENDKEY = "0428f6ebba1f41e6823e80649dce4cb3"

def send_pushplus_alert(message):
    """发送 PushPlus 推送"""
    url = "http://www.pushplus.plus/send"
    data = {
        "token": PUSH_PLUS_SENDKEY,
        "title": "闻泰科技事件监控 - 测试",
        "content": message
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print(f"✅ PushPlus 推送成功")
        else:
            print(f"⚠️ PushPlus 推送失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 推送异常: {e}")

# 测试用例 1: 利好消息
def test_bull_alert():
    print("\n" + "="*50)
    print("🟢 测试 1: 利好警报 (BUY ALERT)")
    print("="*50)
    
    test_message = """
[利好 BUY ALERT]
关键词: 中国全面豁免 Nexperia 芯片出口管制
标题: 速报！中国全面豁免 Nexperia 芯片出口管制，荷兰安世有望恢复大规模出货
来源: https://rss.sina.com.cn/tech/rollnews.xml
"""
    print(test_message)
    send_pushplus_alert(test_message)
    time.sleep(2)

# 测试用例 2: 利空消息
def test_bear_alert():
    print("\n" + "="*50)
    print("🔴 测试 2: 利空警报 (SELL ALERT)")
    print("="*50)
    
    test_message = """
[利空 SELL ALERT]
关键词: 中方重新收紧出口
标题: 最新消息：中方重新收紧芯片出口，Nexperia 面临新一轮制裁
来源: https://feeds.bloomberg.com/technology.rss
"""
    print(test_message)
    send_pushplus_alert(test_message)
    time.sleep(2)

# 测试用例 3: 自定义消息
def test_custom_alert():
    print("\n" + "="*50)
    print("📝 测试 3: 自定义消息")
    print("="*50)
    
    test_message = """
[自定义警报]
这是一条测试消息。
如果你收到了这条通知，说明 PushPlus 推送服务工作正常！
"""
    print(test_message)
    send_pushplus_alert(test_message)
    time.sleep(2)

if __name__ == "__main__":
    print("🚀 闻泰科技事件监控 - 警报测试")
    print("将向 PushPlus 发送测试消息...")
    
    # 运行所有测试
    test_bull_alert()
    test_bear_alert()
    test_custom_alert()
    
    print("\n" + "="*50)
    print("✅ 所有测试完成！")
    print("="*50)
    print("\n提示：")
    print("- 检查你的手机/邮箱是否收到推送")
    print("- 如果收到了，说明监控系统配置正确")
    print("- 如果没收到，请检查 SendKey 是否正确")
