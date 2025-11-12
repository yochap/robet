#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
闻泰科技事件实时监控系统 - 启动器
快速启动监控，包含验证和日志记录
"""

import subprocess
import sys
import os
import datetime

def print_banner():
    """打印启动横幅"""
    print("\n" + "=" * 60)
    print("  🚀 闻泰科技事件实时监控系统")
    print("=" * 60)
    print(f"  启动时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Python 版本: {sys.version.split()[0]}")
    print(f"  工作目录: {os.getcwd()}")
    print("=" * 60 + "\n")

def check_dependencies():
    """检查必要的依赖"""
    print("📋 检查依赖...")
    
    required_packages = {
        'requests': 'HTTP 请求库',
        'bs4': 'HTML 解析库',
    }
    
    missing = []
    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"  ✓ {package:<15} {description}")
        except ImportError:
            print(f"  ✗ {package:<15} {description} [缺失]")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  缺少必要的包: {', '.join(missing)}")
        print("请运行以下命令安装:")
        print(f"  pip install {' '.join(missing)}\n")
        return False
    
    print("\n✅ 所有依赖检查完毕\n")
    return True

def start_monitor():
    """启动监控系统"""
    print("🔄 启动监控系统...\n")
    
    script_path = os.path.join(os.path.dirname(__file__), "import requests.py")
    
    try:
        subprocess.run(
            [sys.executable, script_path],
            check=False
        )
    except KeyboardInterrupt:
        print("\n\n⛔ 监控已停止 (用户中断)")
        print(f"停止时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}\n")
        return False
    
    return True

def main():
    print_banner()
    
    # 检查依赖
    if not check_dependencies():
        return 1
    
    # 启动监控
    start_monitor()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
