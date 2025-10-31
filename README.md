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
- **HTML**: 純結構和樣式 (index.html)
- **資料**: 圖片資料分離 (data.js)
- **邏輯**: JavaScript 功能分離 (app.js)
- **搜尋**: 整合搜尋功能 (search-all.js)

### **外部依賴**：
- Bootstrap 5.3.0 (CDN)
- Bootstrap Icons 1.10.0 (CDN)

## 🚀 快速開始

### 部署使用
1. 將 `index.html`、`data.js`、`app.js`、`search-all.js` 檔案上傳到 HTTPS 伺服器
2. 使用 `index.html` 作為主頁面
3. 系統會自動載入 `data.js`、`app.js` 和 `search-all.js`

### GitHub Pages 部署
1. 在 GitHub 專案頁面，進入 Settings > Pages
2. 選擇 "Deploy from a branch"
3. 選擇 "main" 分支和 "/ (root)" 資料夾
4. 點擊 Save，等待部署完成
5. 您的網站將在 `https://您的用戶名.github.io/udnPicdownload/` 上線

### 資料更新
```bash
# 進入腳本目錄
cd scripts

# 直接執行 Python 腳本
python update_data_auto.py
```

## 📁 專案結構

```
udnPicdownload/
├── index.html              # 主頁面檔案
├── data.js                 # 圖片資料檔案
├── app.js                  # JavaScript 邏輯檔案
├── search-all.js           # 整合搜尋功能檔案
├── scripts/                # 更新腳本
│   ├── update_data_auto.py     # 自動更新腳本（亦可本機執行）
│   ├── update_data_backup.py   # 備份/簡化版本（保險機制）
│   └── log_server.py           # 前端日誌伺服器
├── docs/                   # 文件檔案
│   ├── 問卷需求.txt        # 問卷需求文件
│   └── 資料更新需求.txt    # 資料更新需求文件
├── requirements/           # 依賴檔案
│   └── requirements.txt    # Python 依賴
├── backups/                # 備份檔案
│   └── data.js.backup_20251021_170639    # data.js 備份檔案
├── logs/                   # 日誌檔案
│   ├── update_data.log     # 資料更新日誌
│   └── front_logs.log      # 前端錯誤日誌
└── .github/workflows/      # GitHub Actions
    └── update-data.yml     # 自動更新工作流程
```

## ✨ 主要功能

- ✅ **5個主題分類**: 健康促進、社會連結、世代共融、友善環境、永續發展
- ✅ **響應式設計**: 適配各種螢幕尺寸
- ✅ **全站整合搜尋**: 跨分類關鍵字搜尋，顯示所有符合條件的圖片
- ✅ **分類內搜尋**: 各分類頁籤內支援關鍵字過濾
- ✅ **分批載入**: 每次載入20張圖片，提升效能
- ✅ **圖片下載**: 支援 Blob 下載功能
- ✅ **自動更新**: 從 Google Sheets 自動同步資料
- ✅ **編碼修正**: 解決繁體中文編碼問題
- ✅ **錯誤日誌**: 前端錯誤自動發送到後端並記錄到 `logs/front_logs.log` 檔案

## 📊 資料統計

- **健康促進**: 94張圖片
- **社會連結**: 57張圖片
- **世代共融**: 15張圖片
- **友善環境**: 19張圖片
- **永續發展**: 6張圖片
- **總計**: 191張圖片

## 🔄 資料更新系統

### **自動更新機制**
系統具備完整的資料更新機制，可從 Google Sheets 自動讀取最新資料並更新 `data.js` 檔案。

### **Google Sheets 資料來源**
- **URL**: https://docs.google.com/spreadsheets/d/1U98cnItKs0hkKLY-l7kGuKxIM0Mf6DBRPSzBHxTI0EY/edit?gid=1594065956#gid=1594065956
- **格式**: CSV 匯出
- **編碼**: 已處理 UTF-8 編碼問題

### **欄位對應**（已支援欄名模糊比對與容錯）
| Google Sheets 欄位 | data.js 欄位 | 說明 |
|-------------------|-------------|------|
| 主編號 | id (前綴) | 英文字母部分 |
| 編號 | id (後綴) | 數字部分，不足位數補0 |
| URL | url | 圖片網址 |
| 主題 | title | 主題名稱 |
| 次主題（圖名） | subtitle | 圖說（亦支援：副標/副標題/小標/說明/敘述/描述） |
| 關鍵字（、區隔） | keywords | 關鍵字（亦支援：關鍵詞/作品編號關鍵字/tags/標籤） |
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
1. 使用 `scripts/update_data_auto.py` 腳本自動更新
2. 或手動修改 `data.js` 檔案
3. 保持 JavaScript 物件結構不變
4. 重新上傳檔案

### **修改功能邏輯**：
1. 編輯 `app.js` 檔案
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

4. **編碼與亂碼問題**
   - 使用 `scripts/update_data_auto.py` 或 `update_data_backup.py`
   - 已處理 UTF-8 with BOM 與常見亂碼樣態
   - 關鍵字自動正規化：統一分隔符為「、」，移除連續分隔與前後多餘符號
   - 無效圖片 URL 會被略過並記錄於日誌

### **日誌與備份**
更新過程會產生 `logs/update_data.log` 日誌檔案，並自動將舊版 `data.js` 備份到 `backups/` 目錄。包含：
- 執行時間
- 資料獲取狀態
- 轉換過程
- 錯誤訊息

### **前端錯誤日誌**
前端錯誤會自動發送到後端 API 並寫入 `logs/front_logs.log` 檔案。包含：
- 錯誤發生時間
- 錯誤來源檔案
- 錯誤訊息
- 使用者瀏覽器資訊
- 發生錯誤的頁面 URL

**啟動日誌伺服器**：

```bash
cd scripts
python log_server.py [埠號]
# 預設埠號為 8080
```

**注意**：
- 如果是純靜態網站（如 GitHub Pages），需要部署額外的後端服務來接收日誌
- 若無後端服務，前端會靜默處理錯誤，不影響使用者體驗
- 日誌格式類似 `update_data.log`：`YYYY-MM-DD HH:MM:SS - ERROR - [檔案名] 錯誤訊息 | URL: ... | UserAgent: ...`

## 🔄 最新更新 (v1.7)

### **Bug 修正**：
- **修正搜尋功能數據結構錯誤** (`search-all.js`)：
  - 修正變數名稱：`window.data` → `window.imageData`
  - 修正圖片屬性：`item.image` → `item.url`
  - 修正描述屬性：`item.description` → `item.subtitle`
  - 修正關鍵字屬性：`item.tags` → `item.keywords`（並正確處理字串轉陣列）
  - 確保與 `data.js` 和 `app.js` 的數據結構一致

### **程式碼品質改進**：
- 移除未使用的變數：`searchAllContainer`（已註解，避免 linter 警告）
- 改善錯誤處理機制：
  - 將阻塞式 `alert` 改為非阻塞式錯誤處理
  - 添加 console 錯誤記錄
  - **前端錯誤日誌系統**：前端錯誤會自動發送到後端 API，寫入 `logs/front_logs.log` 檔案
  - 在畫面顯示友善的錯誤訊息給使用者
  - 若無後端 API，錯誤會靜默失敗不影響使用者體驗

### **功能改進**：
- **搜尋功能整合**：`search-all.js` 現在可正確與 `app.js` 的 `openImageModal` 函數整合
- **錯誤日誌系統**：
  - 前端錯誤會自動發送到 `/api/log-front-error` API
  - 後端接收後寫入 `logs/front_logs.log` 檔案
  - 提供 Python 後端伺服器範例 (`scripts/log_server.py`)

## 🔄 歷史更新 (v1.6)

### **系統優化**：
- 日誌路徑統一為 `logs/update_data.log`；備份統一於 `backups/`
- 移除批次腳本教學（`update.sh`/`update.bat`），統一以 Python 執行
- 精準處理繁中亂碼並加入關鍵字正規化
- 補強 URL 合法性檢查與日誌記錄
- README 說明同步更新

### **UI/UX 改進**：
- **下載按鈕樣式統一**: 將「可直接使用」圖片的下載按鈕區塊樣式統一為與「使用限制」區塊相同的設計
  - 新增灰色區塊背景
  - 加入標題和說明文字
  - 統一樣式風格
- **分頁說明文字框**: 新增每個分頁的說明文字區塊
  - 位置：圖片網格上方
  - 樣式：淺綠色卡片設計（#f0f8f0 背景，深綠色邊框）
  - 內容：根據各分頁主題提供相應說明文字
  - 響應式設計：手機版自動調整
- **說明文字框尺寸優化**: 調整說明文字框大小與頁籤邊緣切齊
  - 最大寬度限制為 600px
  - 置中對齊顯示
  - 與第一、第五頁籤邊緣對齊
- **說明文字樣式簡化**: 移除說明文字框的背景和邊框設計
  - 移除淺綠色背景和邊框
  - 移除圓角和陰影效果
  - 文字改為黑色粗體顯示
  - 字體大小從 16px 加大為 18px
  - 手機版字體大小調整為 16px

### **功能改進**：
- **圖卡簡化**: 移除標題、副標題、hashtag，僅保留圖片
- **下載優化**: 改用 Blob 下載，避免瀏覽器僅開啟新分頁
- **UI 改善**: Modal 關閉按鈕加入白色 X 圖示
- **標題結構**: 確認主標題與副標題正確分行顯示
- **編碼修正**: 解決 Google Sheets 資料的繁體中文編碼問題
- **文字顏色優化**: 調整使用限制說明文字顏色
  - 需要申請：灰色文字 (#6c757d)
  - 可直接使用：綠色文字 (#198754)
  - 說明文字：黑色粗體文字 (#000000)

### **技術改進**：
- 優化 `createImageCard` 函數，簡化 DOM 結構
- 重寫下載邏輯，支援跨域圖片下載
- 加入錯誤處理與後備方案
- 新增自動資料更新系統
- 支援 GitHub Actions 自動部署
- 新增 CSS 樣式類別：`.description-block`、`.description-content`
- 響應式設計優化：手機版樣式調整

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
1. **本機測試**: 使用 `scripts/update_data_auto.py`
2. **生產環境**: 使用 GitHub Actions 自動更新

### **注意事項**：
- 每次更新會自動備份現有 `data.js` 檔案到 `backups/` 目錄
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
1. 日誌檔案 `logs/update_data.log`（資料更新日誌）
2. 日誌檔案 `logs/front_logs.log`（前端錯誤日誌）
3. GitHub Actions 執行記錄
4. Google Sheets 資料格式（表頭建議：主編號、編號、主題、次主題（圖名）、圖片URL/URL、關鍵字、使用限制）
5. 瀏覽器 Console 錯誤訊息

## 🔄 更新時間

- **自動更新**: 每日中午12點
- **手動更新**: 隨時可執行
- **GitHub 部署**: 自動觸發

---
**版本**: v1.7  
**更新日期**: 2025年1月7日  
**維護者**: Kevin Tsai
