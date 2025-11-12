# ⚙️ 闻泰科技监控系统 - 配置和启动指南

## 🎉 验证成功！系统已就绪

你已经成功验证了推送系统！现在可以开始正式监控。

## 🚀 快速启动

### Windows 用户（最简单）
1. 打开 `start_monitor.bat` 双击运行
2. 系统会自动启动监控
3. 将保持运行直到你手动关闭

### 所有用户（通用方式）
```bash
# 方式 1: 运行启动器
python start_monitor.py

# 方式 2: 直接运行监控脚本
python "import requests.py"
```

## 📊 监控系统工作流程

```
启动脚本
  ↓
检查依赖 (requests, BeautifulSoup4)
  ↓
加载配置 (关键词、新闻源、SendKey)
  ↓
进入主循环 (每 10 分钟运行一次)
  ├─ 并行抓取 17 个新闻源
  ├─ 提取标题和链接
  ├─ 匹配关键词
  └─ 触发警报推送
  ↓
继续监控...
```

## 🔧 重要配置

### 1. 修改监控间隔
打开 `import requests.py`，找到第 59 行：
```python
INTERVAL = 600  # 改为其他值（单位：秒）

# 常用配置:
INTERVAL = 60    # 1 分钟 - 快速响应（高频率）
INTERVAL = 300   # 5 分钟 - 平衡方案
INTERVAL = 600   # 10 分钟 - 默认值（推荐）
INTERVAL = 1800  # 30 分钟 - 低频率
```

### 2. 添加更多关键词
在 `import requests.py` 找到关键词列表：

**添加利好关键词** (第 37-50 行)：
```python
BULL_KEYWORDS = [
    # ... 已有的关键词 ...
    "新增的关键词1",
    "新增的关键词2",
]
```

**添加利空关键词** (第 52-58 行)：
```python
BEAR_KEYWORDS = [
    # ... 已有的关键词 ...
    "新增的关键词1",
]
```

### 3. 添加新闻源
在 `import requests.py` 第 27-46 行修改 `NEWS_URLS`：

```python
NEWS_URLS = [
    "https://现有的新闻源",
    "https://新增的新闻源1",
    "https://新增的新闻源2",
]
```

推荐的新闻源：
- 股票论坛: https://guba.eastmoney.com/
- 雪球: https://xueqiu.com/
- 同花顺: https://www.10jqka.com.cn/
- 爱好者: https://www.xtcaijing.com/

## 📱 推送设置

### PushPlus 推送配置
当前配置的 SendKey: `0428f6ebba1f41e6823e80649dce4cb3`

如果需要修改或添加新的推送方式：

1. **修改 SendKey**
   打开 `import requests.py` 第 60 行：
   ```python
   PUSH_PLUS_SENDKEY = "你的新SendKey"
   ```

2. **获取新的 SendKey**
   - 访问 https://www.pushplus.plus/
   - 注册或登录
   - 复制你的 SendKey

3. **测试推送**
   随时可以改回 `TEST_MODE = True` 再次验证

## 💾 后台运行（可选）

### Windows 任务计划程序
1. 按 `Win + R`，输入 `taskschd.msc`
2. 点击 "创建基本任务"
3. 名称输入: `闻泰科技监控`
4. 触发器: 选择 "当系统启动时"
5. 操作: 选择 "启动程序"
   - 程序: `C:\Users\pc\Desktop\robet\start_monitor.bat`

### Linux/Mac 后台运行
```bash
# 使用 nohup 后台运行
nohup python "import requests.py" > monitor.log 2>&1 &

# 或使用 screen
screen -S monitor
python "import requests.py"
# 按 Ctrl+A 再按 D 分离
```

## 🔍 监控结果查看

### 查看实时日志
监控运行时会输出：
```
🔄 第 1 轮抓取 - 14:30:05
✓ 成功抓取 https://rss.sina.com.cn/tech/rollnews.xml (145 条标题)
✅ [利好 BUY ALERT]
关键词: 中国全面豁免 Nexperia 芯片出口管制
标题: 速报：中国全面豁免 Nexperia 芯片出口管制
📊 本轮结果: 成功抓取 12 个源，触发 1 个警报
```

### 推送验证
- 所有警报都会通过 PushPlus 推送到你的手机/邮箱
- 推送内容包括: 警报类型、关键词、新闻标题、来源

## ⚠️ 常见问题

### Q: 可以同时运行多个脚本吗？
A: 可以，但每次爬取会占用网络带宽，建议只运行一个。

### Q: 如何停止监控？
A: 在命令行按 `Ctrl + C` 即可停止。

### Q: 关键词匹配是否区分大小写？
A: 不区分，系统会自动转小写比对。

### Q: 如果某个新闻源无法访问怎么办？
A: 不影响其他源，系统会自动跳过并继续。

### Q: 如何修改推送时间？
A: `INTERVAL` 参数控制，默认 600 秒（10 分钟）。

## 📝 文件说明

```
robet/
├── import requests.py          # 主监控脚本
├── start_monitor.py            # 启动器（检查依赖）
├── start_monitor.bat           # Windows 快捷启动
├── test_alerts.py              # 测试脚本
├── README.md                   # 使用说明
├── CONFIG_GUIDE.md             # 本文件
└── monitor.log                 # 监控日志（自动生成）
```

## 🎯 下一步建议

1. ✅ **已完成**: 验证推送系统正常
2. 📋 **准备**: 根据需要调整关键词和间隔
3. 🚀 **启动**: 运行 `start_monitor.bat` 开始监控
4. 📊 **监控**: 等待警报推送，实时跟踪事件

## 📞 技术支持

- PushPlus 帮助: https://www.pushplus.plus/
- Python requests: https://requests.readthedocs.io/
- BeautifulSoup4: https://www.crummy.com/software/BeautifulSoup/

---

**祝监控顺利！** 🎉

任何问题随时可以调整配置。
