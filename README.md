# 新醫情圖庫

## 📋 專案說明
因需要嵌入至feversocial後台嵌入區塊，但該區塊有5000字長度限制，因此修改了原始檔案結構，同時部署至github，後續可以iframe方式嵌入，解決原始版本 JavaScript 超過 5000 字限制的問題。

## ✅ 優化成果

### **Embed 限制解決**：
- **原始版本**: JavaScript 64,177 字元 ❌ (超過限制 12.8 倍)
- **優化版本**: JavaScript 0 字元 ✅ (完全符合限制)

### **檔案大小對比**：
| 版本 | 總大小 | JavaScript 字數 | 狀態 |
|------|--------|----------------|------|
| 原始 | 82.9KB | 64,177 字元 | ❌ 超過限制 |
| 優化 | 74.9KB | 0 字元 | ✅ 符合限制 |

## 🛠️ 技術架構

### **分離式架構**：
- **HTML**: 純結構和樣式 (src/index.html)
- **資料**: 圖片資料分離 (src/data.js)
- **邏輯**: JavaScript 功能分離 (src/app.js)

### **外部依賴**：
- Bootstrap 5.3.0 (CDN)
- Bootstrap Icons 1.10.0 (CDN)

## 🚀 快速開始

### 部署使用
1. 將 `src/` 目錄中的所有檔案上傳到 HTTPS 伺服器
2. 使用 `src/index.html` 作為主頁面
3. 系統會自動載入 `src/data.js` 和 `src/app.js`

### 資料更新
```bash
# 進入腳本目錄
cd scripts

# Windows 使用者
update.bat

# macOS/Linux 使用者
chmod +x update.sh && ./update.sh

# 或直接執行 Python 腳本
python update_data_final.py
```

## 📁 專案結構

```
udnPicdownload/
├── src/                    # 主要程式檔案
│   ├── index.html          # 主頁面檔案
│   ├── data.js             # 圖片資料檔案
│   └── app.js              # JavaScript 邏輯檔案
├── scripts/                # 更新腳本
│   ├── update_data_final.py    # 主要更新腳本（推薦使用）
│   ├── update_data.py          # 原始更新腳本
│   ├── update_data_simple.py   # 簡化版本
│   ├── update.sh               # Linux/macOS 執行腳本
│   └── update.bat              # Windows 執行腳本
├── docs/                   # 文件檔案
│   ├── README.md           # 完整專案說明文件
│   ├── 問卷需求.txt        # 問卷需求文件
│   └── 資料更新需求.txt    # 資料更新需求文件
├── requirements/           # 依賴檔案
│   └── requirements.txt    # Python 依賴
├── backups/                # 備份檔案
│   └── data.js.backup_*    # data.js 最新備份檔案
├── logs/                   # 日誌檔案
│   └── update_data.log     # 更新日誌
└── .github/workflows/      # GitHub Actions
    └── update-data.yml     # 自動更新工作流程
```

## ✨ 主要功能

- ✅ **5個主題分類**: 健康促進、社會連結、世代共融、友善環境、永續發展
- ✅ **響應式設計**: 適配各種螢幕尺寸
- ✅ **模糊搜尋**: 支援關鍵字搜尋
- ✅ **分批載入**: 每次載入20張圖片，提升效能
- ✅ **圖片下載**: 支援 Blob 下載功能
- ✅ **自動更新**: 從 Google Sheets 自動同步資料
- ✅ **編碼修正**: 解決繁體中文編碼問題

## 📊 資料統計

- **健康促進**: 96張圖片
- **社會連結**: 57張圖片
- **世代共融**: 16張圖片
- **友善環境**: 19張圖片
- **永續發展**: 6張圖片
- **總計**: 194張圖片

## 🔄 資料更新系統

### **自動更新機制**
系統具備完整的資料更新機制，可從 Google Sheets 自動讀取最新資料並更新 `src/data.js` 檔案。

### **Google Sheets 資料來源**
- **URL**: https://docs.google.com/spreadsheets/d/1U98cnItKs0hkKLY-l7kGuKxIM0Mf6DBRPSzBHxTI0EY/edit?gid=1594065956#gid=1594065956
- **格式**: CSV 匯出
- **編碼**: 已處理 UTF-8 編碼問題

### **欄位對應**
| Google Sheets 欄位 | data.js 欄位 | 說明 |
|-------------------|-------------|------|
| 主編號 | id (前綴) | 英文字母部分 |
| 編號 | id (後綴) | 數字部分，不足位數補0 |
| URL | url | 圖片網址 |
| 主題 | title | 主題名稱 |
| 次主題（圖名） | subtitle | 圖說 |
| 關鍵字（、區隔） | keywords | 關鍵字 |
| 使用限制 | restriction | 使用限制狀態 |

### **主題對應**
| 主題名稱 | 編號 | 說明 |
|---------|------|------|
| 健康促進 | 1 | 健康相關圖片 |
| 社會連結 | 2 | 社會連結相關圖片 |
| 世代共融 | 3 | 世代共融相關圖片 |
| 友善環境 | 4 | 友善環境相關圖片 |
| 永續發展 | 5 | 永續發展相關圖片 |

### **GitHub Actions 自動更新**
系統已設定 GitHub Actions 工作流程，會：
- **每日中午12點**自動執行更新
- 支援**手動觸發**更新
- 自動提交變更到 GitHub
- 產生更新報告

#### 手動觸發
在 GitHub 專案頁面：
1. 點擊 "Actions" 標籤
2. 選擇 "自動更新圖庫資料" 工作流程
3. 點擊 "Run workflow" 按鈕

## 🔧 維護說明

### **更新圖片資料**：
1. 使用 `scripts/update_data_final.py` 腳本自動更新
2. 或手動修改 `src/data.js` 檔案
3. 保持 JavaScript 物件結構不變
4. 重新上傳檔案

### **修改功能邏輯**：
1. 編輯 `src/app.js` 檔案
2. 保持函數名稱和事件綁定不變
3. 重新上傳檔案

## 🔧 故障排除

### **常見問題**

1. **Google Sheets 存取失敗**
   - 確認 Google Sheets 為公開狀態
   - 檢查網路連線

2. **Python 環境問題**
   - 確認已安裝 Python 3.7+
   - 執行 `pip install -r requirements/requirements.txt`

3. **權限問題**
   - 確認檔案寫入權限
   - 檢查 GitHub Actions 權限設定

4. **編碼問題**
   - 使用 `scripts/update_data_final.py` 腳本
   - 該腳本已處理 Google Sheets 的編碼問題

### **日誌檔案**
更新過程會產生 `logs/update_data.log` 日誌檔案，包含：
- 執行時間
- 資料獲取狀態
- 轉換過程
- 錯誤訊息

## 🔄 最新更新 (v1.2)

### **功能改進**：
- **圖卡簡化**: 移除標題、副標題、hashtag，僅保留圖片
- **下載優化**: 改用 Blob 下載，避免瀏覽器僅開啟新分頁
- **UI 改善**: Modal 關閉按鈕加入白色 X 圖示
- **標題結構**: 確認主標題與副標題正確分行顯示
- **編碼修正**: 解決 Google Sheets 資料的繁體中文編碼問題

### **技術改進**：
- 優化 `createImageCard` 函數，簡化 DOM 結構
- 重寫下載邏輯，支援跨域圖片下載
- 加入錯誤處理與後備方案
- 新增自動資料更新系統
- 支援 GitHub Actions 自動部署

## 🎯 使用建議

### **Embed 平台**：
- ✅ 完全符合 5000 字限制
- ✅ 支援 HTTPS 外部檔案引用
- ✅ 響應式設計適配各種螢幕

### **瀏覽器相容性**：
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### **下載功能**：
- ✅ 支援直接下載圖片檔案
- ✅ 自動偵測檔案副檔名
- ✅ CORS 限制時提供後備方案

### **推薦使用方式**：
1. **本機測試**: 使用 `scripts/update_data_final.py`
2. **生產環境**: 使用 GitHub Actions 自動更新
3. **緊急更新**: 使用本機腳本手動更新

### **注意事項**：
- 每次更新會自動備份現有 `src/data.js` 檔案到 `backups/` 目錄
- 更新過程會產生詳細日誌到 `logs/` 目錄
- 建議在更新前檢查 Google Sheets 資料完整性

## 🛠️ 技術規格

- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **框架**: Bootstrap 5.3.0
- **圖示**: Bootstrap Icons 1.10.0
- **後端更新**: Python 3.7+
- **資料來源**: Google Sheets API
- **部署**: GitHub Pages / HTTPS 伺服器

## 📞 支援

如有問題，請檢查：
1. 日誌檔案 `logs/update_data.log`
2. GitHub Actions 執行記錄
3. Google Sheets 資料格式

## 🔄 更新時間

- **自動更新**: 每日中午12點
- **手動更新**: 隨時可執行
- **GitHub 部署**: 自動觸發

---
**版本**: v1.2  
**更新日期**: 2025年10月21日  
**維護者**: UDN Frontend Team
