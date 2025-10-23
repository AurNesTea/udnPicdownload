@echo off
REM 新醫情圖庫資料更新腳本 - Windows 版本

echo 🚀 開始更新新醫情圖庫資料...

REM 檢查 Python 環境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 錯誤: 未找到 Python，請先安裝 Python
    pause
    exit /b 1
)

REM 檢查並安裝依賴
echo 📦 檢查並安裝依賴套件...
pip install -r ../requirements/requirements.txt

REM 執行更新腳本
echo 🔄 執行資料更新...
python update_data_auto.py

if errorlevel 1 (
    echo ❌ 資料更新失敗，請檢查日誌檔案
    pause
    exit /b 1
) else (
    echo ✅ 資料更新完成！
    echo 📁 更新檔案: data.js
    echo 📋 備份檔案: data.js.backup_*
    echo 📝 日誌檔案: update_data.log
    pause
)
