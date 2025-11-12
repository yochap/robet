# 🎯 快速参考卡

## 启动监控系统

### 最简单的方式（Windows）
```bash
双击打开: start_monitor.bat
```

### 命令行启动
```bash
cd c:\Users\pc\Desktop\robet
python start_monitor.py
```

---

## 常见操作

### 1. 修改监控间隔
编辑 `import requests.py` 第 59 行
```python
INTERVAL = 300  # 改为 5 分钟（单位：秒）
```

### 2. 测试推送功能
编辑 `import requests.py` 第 63 行
```python
TEST_MODE = True  # 改为 True，运行后自动发送测试消息
```

### 3. 添加新关键词
编辑 `import requests.py`，在对应列表后添加
```python
BULL_KEYWORDS = [
    # ... 已有的 ...
    "你的新关键词",  # 添加这里
]
```

### 4. 修改推送 SendKey
编辑 `import requests.py` 第 60 行
```python
PUSH_PLUS_SENDKEY = "你的新SendKey"
```

---

## 文件一览

| 文件 | 说明 | 用途 |
|------|------|------|
| `import requests.py` | 主监控脚本 | 核心功能，包含所有配置 |
| `start_monitor.py` | 启动器 | 依赖检查和启动管理 |
| `start_monitor.bat` | 批处理文件 | Windows 一键启动 |
| `test_alerts.py` | 测试脚本 | 验证警报功能 |
| `README.md` | 使用说明 | 功能和触发原理 |
| `CONFIG_GUIDE.md` | 配置指南 | 详细配置说明 |

---

## 快速问题排查

### ❌ 没有收到推送
- [ ] 检查网络连接
- [ ] 验证 SendKey 正确性
- [ ] 运行 TEST_MODE 测试推送

### ❌ 显示 HTTP 错误（403/401）
- [ ] 这是正常现象（某些网站禁止爬虫）
- [ ] 系统会自动尝试其他源
- [ ] 可以添加更多新闻源

### ❌ 没有触发警报
- [ ] 检查关键词是否拼写正确
- [ ] 确认新闻源有内容更新
- [ ] 试试降低 INTERVAL 增加检查频率

---

## ✨ 系统状态

| 项目 | 状态 |
|------|------|
| 推送系统 | ✅ 已验证正常 |
| 测试模式 | ❌ 已关闭 |
| 关键词 | ✅ 已配置 |
| 新闻源 | ✅ 已配置（17 个） |
| 监控间隔 | ✅ 600 秒（10 分钟） |

---

## 🚀 立即开始

```powershell
# Windows PowerShell
cd C:\Users\pc\Desktop\robet
.\start_monitor.bat

# 或直接运行
python "import requests.py"
```

按 `Ctrl + C` 停止监控

---

**最后更新**: 2025-11-12  
**版本**: 2.0  
**状态**: ✅ 生产就绪
