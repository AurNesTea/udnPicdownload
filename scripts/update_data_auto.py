#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新醫情圖庫資料更新腳本
從 Google Sheets 讀取資料並更新 data.js 檔案
"""

import os
import json
import requests
import logging
import re
from datetime import datetime
from typing import Dict, List, Any
from urllib.parse import urlparse

# 設定路徑：以腳本所在位置推導專案根目錄，避免執行位置造成路徑錯誤
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))

# 設定日誌輸出至專案根目錄檔案
log_file = os.path.join(REPO_ROOT, 'logs/update_data.log')
os.makedirs(os.path.dirname(log_file), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DataUpdater:
    def __init__(self):
        self.sheets_url = "https://docs.google.com/spreadsheets/d/1U98cnItKs0hkKLY-l7kGuKxIM0Mf6DBRPSzBHxTI0EY/edit?gid=1594065956#gid=1594065956"
        self.csv_url = "https://docs.google.com/spreadsheets/d/1U98cnItKs0hkKLY-l7kGuKxIM0Mf6DBRPSzBHxTI0EY/export?format=csv&gid=1594065956"
        # 將輸出檔、備份與日誌統一至專案根目錄
        self.output_file = os.path.join(REPO_ROOT, 'data.js')
        self._http = requests.Session()
        self._http.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; DataUpdater/1.0; +https://example.com)"
        })
        
    def fetch_data_from_sheets(self) -> List[Dict[str, Any]]:
        """從 Google Sheets 獲取資料（正確處理 UTF-8）"""
        import csv, io
        logger.info("正在從 Google Sheets 獲取資料...")

        r = self._http.get(self.csv_url, timeout=30)
        r.raise_for_status()

        # 用 bytes，自行以 UTF-8（含 BOM）解碼
        csv_text = r.content.decode("utf-8-sig", errors="strict")
        reader = csv.DictReader(io.StringIO(csv_text))
        data = [row for row in reader]
        logger.info(f"成功獲取 {len(data)} 筆資料")
        return data
    
    def transform_data(self, raw_data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """將原始資料轉換為 data.js 格式"""
        logger.info("正在轉換資料格式...")
        
        # 主題對應表（使用正確的繁體中文）
        theme_mapping = {
            "健康促進": 1,
            "社會連結": 2,
            "世代共融": 3,
            "友善環境": 4,
            "永續發展": 5
        }
        
        # 初始化各主題的資料陣列
        image_data = {str(i): [] for i in range(1, 6)}
        
        def is_valid_url(url: str) -> bool:
            try:
                parsed = urlparse(url)
                return parsed.scheme in ("http", "https") and bool(parsed.netloc)
            except Exception:
                return False

        def normalize_keywords(text: str) -> str:
            if not text:
                return text
            t = text.strip()
            # 統一為頓號作為分隔
            t = t.replace(",", "、").replace("，", "、")
            # 合併連續頓號
            t = re.sub(r"、{2,}", "、", t)
            # 去除前後多餘頓號與空白
            t = t.strip("、 ")
            return t

        # 欄名對應，避免欄位順序變動造成錯誤
        field_map: Dict[str, List[str]] = {
            "main_id": ["主編號", "主編號ID"],
            "sub_id": ["編號", "次編號"],
            "theme": ["主題"],
            "subtitle": ["副標", "副標題", "次主題（圖名）"],
            "url": ["圖片URL", "URL", "連結", "圖片連結"],
            "keywords": ["關鍵字", "關鍵詞", "關鍵字（、區隔）", "tags", "標籤"],
            "restriction": ["使用限制", "權限"],
        }

        def pick(row: Dict[str, Any], candidates: List[str], default: str = "") -> str:
            for name in candidates:
                if name in row and row[name] is not None:
                    return str(row[name]).strip()
            return default

        for row in raw_data:
            try:
                # 依欄名取值（避免欄序變動）
                main_id      = pick(row, field_map["main_id"])
                sub_id       = pick(row, field_map["sub_id"])
                theme_raw    = pick(row, field_map["theme"])
                subtitle     = pick(row, field_map["subtitle"])
                url          = pick(row, field_map["url"])
                keywords     = pick(row, field_map["keywords"])
                restriction  = pick(row, field_map["restriction"], "無限制")

                 # 主題名稱容錯（去全形空白/多餘空白）
                theme = theme_raw.replace("\u3000", "").strip()

                # 驗證必要欄位
                if not all([main_id, sub_id, url, theme]):
                    logger.warning(f"跳過不完整的資料行: 主編號={main_id}, 編號={sub_id}, 主題={theme}")
                    continue
                # 生成圖片 ID
                image_id = f"{main_id}{sub_id.zfill(3)}"

                # 驗證 URL 合法性（例如 C008 錯誤 URL）
                if not is_valid_url(url):
                    logger.warning(f"無效的圖片 URL，已略過輸出: 圖片ID={image_id}, URL={url}")
                    continue
                
                # 取得主題編號
                theme_number = theme_mapping.get(theme)
                if not theme_number:
                    logger.warning(f"未知的主題: {theme} (原始: {theme_raw})")
                    continue
                
                # 正規化關鍵字（移除重複分隔與多餘空白）
                keywords = normalize_keywords(keywords)

                # 建立圖片資料物件
                image_obj = {
                    "id": image_id,
                    "url": url,
                    "title": theme,
                    "subtitle": subtitle,
                    "keywords": keywords,
                    "restriction": restriction
                }
                # 加入對應主題
                image_data[str(theme_number)].append(image_obj)
                    
            except Exception as e:
                logger.error(f"處理資料行時發生錯誤: {e}")
                continue
        
        # 統計各主題圖片數量
        for theme_num, images in image_data.items():
            logger.info(f"主題 {theme_num}: {len(images)} 張圖片")
        
        return image_data
    
    def generate_data_js(self, image_data: Dict[str, List[Dict[str, Any]]]) -> str:
        """生成 data.js 檔案內容"""
        logger.info("正在生成 data.js 檔案...")
        
        # 生成檔案頭部註解
        timestamp = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        header = f"""// 圖片資料 - 根據Google Sheets「新醫情圖庫資料表」的實際資料
// 最後更新時間: {timestamp}
// 自動生成，請勿手動修改

const imageData = {{
"""
        
        # 生成各主題資料
        content_parts = []
        for theme_num in range(1, 6):
            images = image_data.get(str(theme_num), [])
            theme_names = {
                1: "健康促進",
                2: "社會連結", 
                3: "世代共融",
                4: "友善環境",
                5: "永續發展"
            }
            
            content_parts.append(f"    {theme_num}: [ // {theme_names[theme_num]} - {len(images)}張圖片")
            
            for img in images:
                # 處理特殊字元，避免 JavaScript 語法錯誤
                img_id = str(img["id"]).replace('"', '\\"').replace("'", "\\'")
                img_url = str(img["url"]).replace('"', '\\"').replace("'", "\\'")
                img_title = str(img["title"]).replace('"', '\\"').replace("'", "\\'")
                img_subtitle = str(img["subtitle"]).replace('"', '\\"').replace("'", "\\'")
                img_keywords = str(img["keywords"]).replace('"', '\\"').replace("'", "\\'")
                img_restriction = str(img["restriction"]).replace('"', '\\"').replace("'", "\\'")
                
                content_parts.append(
                    f'        {{ id: "{img_id}", url: "{img_url}", title: "{img_title}", subtitle: "{img_subtitle}", keywords: "{img_keywords}", restriction: "{img_restriction}" }},'
                )
            
            content_parts.append("    ],")
        
        # 組合完整內容
        content = header + "\n".join(content_parts)
        content = content.rstrip(",\n") + "\n};\n\n" \
            "// 確保 imageData 在全域作用域中可存取（供 search-all.js 使用）\n" \
            "if (typeof window !== \"undefined\") {\n" \
            "    window.imageData = imageData;\n" \
            "}\n"
        
        return content
    
    def backup_existing_file(self):
        """備份現有的 data.js 檔案"""
        if os.path.exists(self.output_file):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backups_dir = os.path.join(REPO_ROOT, 'backups')
            os.makedirs(backups_dir, exist_ok=True)
            backup_file = os.path.join(backups_dir, f"{os.path.basename(self.output_file)}.backup_{timestamp}")
            os.rename(self.output_file, backup_file)
            logger.info(f"已備份現有檔案至: {backup_file}")
    
    def update_data_file(self):
        """執行完整的資料更新流程"""
        try:
            logger.info("開始資料更新流程...")
            
            # 1. 從 Google Sheets 獲取資料
            raw_data = self.fetch_data_from_sheets()
            
            # 2. 轉換資料格式
            image_data = self.transform_data(raw_data)
            
            # 3. 生成 data.js 內容
            js_content = self.generate_data_js(image_data)
            
            # 4. 備份現有檔案
            self.backup_existing_file()
            
            # 5. 寫入新檔案
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(js_content)
            
            logger.info(f"資料更新完成！已更新 {self.output_file}")
            
            # 6. 修復亂碼
            # self.fix_garbled_text()
            
            # 7. 驗證檔案
            self.validate_output_file()
            
        except Exception as e:
            logger.error(f"資料更新失敗: {e}")
            raise
    
    # def fix_garbled_text(self):
    #     """修復 data.js 檔案中的亂碼"""
    #     try:
    #         # 讀取檔案內容
    #         with open(self.output_file, 'r', encoding='utf-8') as f:
    #             content = f.read()
            
    #         # 定義亂碼替換規則
    #         replacements = {
    #             "æ\x85¢æ\x80§ç\x97\x85ã\x80\x81ä¸\x89é«\x98ã\x80\x81ç³\x96å°¿ç\x97\x85ã\x80\x81é«\x98è¡\x80å£\x93ã\x80\x81å¿\x83è¡\x80ç®¡ç\x96¾ç\x97\x85ã\x80\x81å\x85¨æ°\x91å\x81¥åº·ä¿\x9dé\x9aªã\x80\x81æ\x95´å\x90\x88ç\x85§è\xad·ã\x80\x81æ\x85¢æ\x80§å\x85±ç\x97": "慢性病、三高、糖尿病、高血壓、心血管疾病、全民健康保險、整合照護、慢性共病"
    #         }
            
    #         # 執行替換
    #         original_content = content
    #         for garbled, correct in replacements.items():
    #             content = content.replace(garbled, correct)
            
    #         # 如果有變更，寫回檔案
    #         if content != original_content:
    #             with open(self.output_file, 'w', encoding='utf-8') as f:
    #                 f.write(content)
    #             logger.info("已修復亂碼文字")
            
    #     except Exception as e:
    #         logger.warning(f"修復亂碼時發生錯誤: {e}")
    
    def validate_output_file(self):
        """驗證生成的 data.js 檔案"""
        try:
            # 讀取檔案內容
            with open(self.output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 檢查基本語法
            if 'const imageData = {' not in content:
                raise ValueError("檔案格式不正確")
            
            logger.info("檔案驗證通過")
            
        except Exception as e:
            logger.error(f"檔案驗證失敗: {e}")
            raise

def main():
    """主程式入口"""
    updater = DataUpdater()
    
    try:
        updater.update_data_file()
        print("✅ 資料更新成功！")
        
    except Exception as e:
        print(f"❌ 資料更新失敗: {e}")
        logger.error(f"更新失敗: {e}")
        exit(1)

if __name__ == "__main__":
    main()
