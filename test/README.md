# 🧪 測試環境說明 (Test Environment)

此資料夾 (`/test`) 用於隔離測試與開發中的新功能，與根目錄正式版有所區別。本次測試的主要目的是驗證 **Modal 的定位與顯示修復**，以及確保從 Embed 平台引用的穩定性。

## 修改重點 (Release Candidate)

### 1. 樣式結構優化
- **CSS 分離**：將原本內嵌於 `<style>` 的樣式抽離為獨立的 `style.css` 檔案，便於維護與除錯。
- **HTML 標準化**：修正 `index.html` 的文件結構 (`<!DOCTYPE>`, `<html>` 標籤)，確保瀏覽器渲染模式正確。

### 2. Modal 行為修正
- **移除自定義定位**：移除了原本為了跟隨滑鼠點擊位置而動態計算 `top` 的 JS 邏輯。
- **回歸 Bootstrap 原生行為**：Modal 現在會使用 Bootstrap 預設的垂直置中與水平置中，解決在不同螢幕尺寸下可能出現的位置偏移或被截斷的問題。

### 3. 手機版優化
- **保留 RWD 設定**：針對手機版解析度 (`max-width: 768px`) 保留了 `.description-block` 的邊距與字型大小優化。

## 使用說明

- 若要預覽測試效果，請直接開啟 `test/index.html`。
- 本地開發時，請確保 `style.css`、`app.js` 與 `data.js` 皆位於同一目錄下。
- **注意**：若測試通過，需將這裡的 `index.html` (需合併 CSS 回去或保留分離架構) 與 `app.js` 的邏輯同步回根目錄的正式版。

## 檔案列表
- `index.html`: 測試版首頁 (引用 `style.css`)
- `style.css`: 測試版樣式表
- `app.js`: 測試版邏輯 (含 Modal 修復)
- `data.js`: 測試版資料 (與正式版共用或獨立拷貝)
