@echo off
chcp 65001 >nul
cls

echo.
echo ================================================
echo   闻泰科技事件实时监控系统 - 启动
echo ================================================
echo.

REM 获取 Python 路径
set PYTHON_PATH=C:\Users\pc\AppData\Local\Programs\Python\Python314\python.exe

REM 检查 Python 是否存在
if not exist "%PYTHON_PATH%" (
    echo ❌ 未找到 Python 可执行文件
    echo 期望位置: %PYTHON_PATH%
    pause
    exit /b 1
)

echo ✓ Python 路径: %PYTHON_PATH%
echo ✓ 当前目录: %cd%
echo.

REM 启动监控
echo 🚀 启动监控系统...
echo.

"%PYTHON_PATH%" "start_monitor.py"

pause
