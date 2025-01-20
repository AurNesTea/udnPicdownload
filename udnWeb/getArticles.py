import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# 設定 Selenium Chrome Driver
options = Options()
options.add_argument("--headless")  # 無頭模式
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# 初始化瀏覽器
driver = webdriver.Chrome(options=options)

def scrape_content(url):
    """從指定的 URL 抓取內文與作者"""
    try:
        driver.get(url)
        time.sleep(random.uniform(3, 6))  # 隨機延遲，模擬用戶行為

        # 使用 BeautifulSoup 解析頁面
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 抓取內文
        content_divs = soup.find_all('div', class_='story__text__wrapper')
        content = ""
        for div in content_divs:
            # 停止於指定的段落結束
            if div.get('style') == "position: relative;margin:50px 0 0;border-radius: 0 0 10px 0;padding: 1em;background-color:#fff;border-radius: 3px":
                break
            content += div.get_text(strip=True) + "\n"

        # 抓取作者名稱
        author_span = soup.find('span', class_='story__content__author')
        author = author_span.get_text(strip=True) if author_span else "未知作者"

        return content.strip(), author
    except Exception as e:
        print(f"錯誤抓取 {url}: {e}")
        return "抓取失敗", "未知作者"

def update_csv(file_path, output_path):
    """從 CSV 文件讀取網址，抓取內容和作者並更新到新欄位"""
    # 讀取 CSV
    df = pd.read_csv(file_path)

    # 確保存在目標欄位
    if '內文' not in df.columns:
        df['內文'] = ''
    if '作者' not in df.columns:
        df['作者'] = ''

    for index, row in df.iterrows():
        url = row['Link']
        if pd.isna(row['內文']) or row['內文'] == '':  # 只處理尚未填寫內文的行
            print(f"正在抓取第 {index + 1} 行的網址: {url}")
            content, author = scrape_content(url)
            df.at[index, '內文'] = content
            df.at[index, '作者'] = author

    # 保存結果到新 CSV 文件
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"抓取完成，結果已保存到 {output_path}")

def main():
    # 輸入 CSV 文件路徑和保存結果的檔案路徑
    csv_file_path = input("請輸入來源 CSV 文件路徑: ").strip()
    output_file_path = input("請輸入保存結果的 CSV 文件路徑: ").strip()

    try:
        update_csv(csv_file_path, output_file_path)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

