from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import random

# 初始化瀏覽器
def init_browser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver

# 隨機等待時間
def random_sleep(min_seconds=1, max_seconds=3):
    time.sleep(random.uniform(min_seconds, max_seconds))

# 模擬人類滾動行為
def human_like_scroll(driver):
    scroll_pause_time = random.uniform(1, 2)  # 每次滾動後的隨機等待時間
    screen_height = driver.execute_script("return window.screen.height;")  # 取得螢幕高度
    i = 1

    while True:
        # 滾動到隨機位置
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        scroll_to = random.randint(int(screen_height * (i - 1)), int(screen_height * i))
        driver.execute_script(f"window.scrollTo(0, {scroll_to});")
        i += 1
        random_sleep(scroll_pause_time, scroll_pause_time + 1)

        # 檢查是否已經滾動到頁面底部
        if screen_height * i > scroll_height:
            break

# 抓取搜尋結果
def scrape_results(driver, max_results):
    results = driver.find_elements(By.CSS_SELECTOR, 'article')
    scraped_data = []

    for result in results[:max_results]:  # 只抓取指定筆數的結果
        title = result.find_element(By.CSS_SELECTOR, 'h2').text
        relative_link = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        
        # 將相對路徑轉換為完整 URL
        if relative_link and not relative_link.startswith('http'):
            full_link = f'https://www.dcard.tw{relative_link}'
        else:
            full_link = relative_link

        scraped_data.append({'title': title, 'link': full_link})

    return scraped_data

# 抓取文章留言回覆內容
def scrape_comments(driver, link):
    driver.get(link)
    random_sleep(5, 7)  # 隨機等待頁面加載

    # 模擬人類滾動行為加載更多留言
    human_like_scroll(driver)

    # 抓取留言回覆內容
    comments = []
    comment_elements = driver.find_elements(By.CSS_SELECTOR, 'div[class^="CommentEntry_container_"]')
    
    for comment in comment_elements:
        content = comment.find_element(By.CSS_SELECTOR, 'div[class^="CommentEntry_content_"]').text
        comments.append(content)

    return comments

# 篩選包含薪資數字的留言
def filter_salary_comments(comments):
    salary_comments = []
    salary_pattern = re.compile(r'\d{1,3}(?:,\d{3})*(?:元|k|K|萬|w|W)')  # 匹配薪資數字

    for comment in comments:
        if salary_pattern.search(comment):
            salary_comments.append(comment)

    return salary_comments

# 主程式
def main():
    # 讓使用者輸入查詢關鍵字和資料筆數
    query = input("請輸入要查詢的關鍵字: ")
    max_results = int(input("請輸入要查詢的資料筆數: "))

    # 根據關鍵字生成搜尋 URL
    url = f'https://www.dcard.tw/search?query={query}&forum=nursing'

    # 初始化瀏覽器
    driver = init_browser()

    try:
        # 打開網頁
        driver.get(url)
        random_sleep(5, 7)  # 隨機等待頁面加載

        # 模擬人類滾動行為加載更多內容
        human_like_scroll(driver)

        # 抓取搜尋結果
        results = scrape_results(driver, max_results)

        # 輸出結果
        print(f"\n找到 {len(results)} 筆結果：")
        for idx, result in enumerate(results, 1):
            print(f"{idx}. 標題: {result['title']}")
            print(f"   連結: {result['link']}")

            # 抓取文章留言回覆內容
            comments = scrape_comments(driver, result['link'])
            salary_comments = filter_salary_comments(comments)

            # 輸出包含薪資數字的留言
            if salary_comments:
                print("   包含薪資數字的留言：")
                for comment in salary_comments:
                    print(f"     - {comment}")
            else:
                print("   沒有包含薪資數字的留言")

            print('---')

    except Exception as e:
        print(f'抓取失敗: {e}')

    finally:
        # 關閉瀏覽器
        driver.quit()

# 執行主程式
if __name__ == "__main__":
    main()