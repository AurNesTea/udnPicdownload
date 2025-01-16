from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time


# 設置 URL 和 WebDriver
domain_url = 'https://health.udn.com'
start_url = 'https://health.udn.com/service/index??type=course'

options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# 儲存抓取的資料
courses = []

try:
    driver.get(start_url)
    
    while True:
        # 等待頁面載入完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'splide__slide'))
        )
        
        # 使用 BeautifulSoup 解析頁面
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # 抓取課程資訊
        course_list = soup.find_all('li', class_='splide__slide card__bottom-left-round__item')
        for cl in course_list:
            course_name = cl.find('a')['title']
            course_link = domain_url + cl.a.get('href')
            course_type = cl.find(
                'a', 
                class_='card__bottom-left-round__link card__bottom-left-round__link--orange'
            ).text.strip()
            
            courses.append({
                '課程名稱': course_name,
                '課程連結': course_link,
                '課程類型': course_type
            })
        
        # 判斷是否存在下一頁按鈕
        next_page_btn = soup.find('a', class_='pagenation__link pagenation__link--last-page')
        if next_page_btn:
            next_page_btn_element = driver.find_element(By.CLASS_NAME, 'pagenation__link--last-page')
            next_page_btn_element.click()
            time.sleep(2)  # 適當延遲，等待頁面加載
        else:
            break  # 如果沒有下一頁按鈕，結束爬取
    
except Exception as e:
    print(f'Error message: {e}')
    
finally:
    # 儲存資料到 CSV
    df = pd.DataFrame(courses)
    df.to_csv('udn_courses.csv', index=False, encoding='utf-8-sig')
    print('任務完成，資料已儲存到 udn_courses.csv')
    driver.quit()