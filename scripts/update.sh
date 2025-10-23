#!/bin/bash
# 新醫情圖庫資料更新腳本 - 本機手動執行版本

echo "🚀 開始更新新醫情圖庫資料..."

# 檢查 Python 環境
if ! command -v python3 &> /dev/null; then
    echo "❌ 錯誤: 未找到 Python3，請先安裝 Python3"
    exit 1
fi

# 檢查並安裝依賴
echo "📦 檢查並安裝依賴套件..."
pip3 install -r ../requirements/requirements.txt

# 執行更新腳本
echo "🔄 執行資料更新..."
python3 update_data_auto.py

if [ $? -eq 0 ]; then
    echo "✅ 資料更新完成！"
    echo "📁 更新檔案: data.js"
    echo "📋 備份檔案: data.js.backup_*"
    echo "📝 日誌檔案: update_data.log"
else
    echo "❌ 資料更新失敗，請檢查日誌檔案"
    exit 1
fi
