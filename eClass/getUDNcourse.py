import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class UdnCourseLink:
    def __init__(self, start_url, domain_url):
        self.start_url = start_url
        self.domain_url = domain_url
        self.course_url_list = []
        self.error_url_list = []
        self.course_teacher_list = []
        self.course_type_list = []
        self.course_price_list = []
        self.intro_course_list = []
        self.intro_teacher_list = []
        self.intro_notice_list = []

        # 設定 Selenium Chrome Driver
        options = Options()
        options.add_argument("--headless")  # 無頭模式
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=options)

    # 主流程
    def scrape_all_page(self):
        self.driver.get(self.start_url)
        time.sleep(random.randint(3, 6))

        while True:
            self.scrape_current_page()
            if not self.click_next_page():
                break
        self.scrape_course_page()

        self.driver.quit()
        self.save_result()
   
    # 取得課程連結
    def scrape_current_page(self):
        course_links = self.driver.find_elements(By.CSS_SELECTOR, 'li.card__bottom-left-round__item')
        for link in course_links:
            href = link.find_element(By.TAG_NAME, 'a').get_attribute('href')
            if not href.startswith('http'):
                course_link = self.domain_url + href
                self.course_url_list.append(course_link)
            else:
                self.course_url_list.append(href)
        print(f"目前已取得 {len(self.course_url_list)} 堂課程連結")

    # 點擊下一頁按鈕
    def click_next_page(self):
        try:
            next_page = self.driver.find_element(By.CSS_SELECTOR, 'a.pagenation__link.pagenation__link--next-page')
            if next_page:
                time.sleep(random.randint(1,3))
                next_page.click()
                print("已點擊下一頁")
                time.sleep(random.randint(1,3))
                return True
        except Exception as e:
            print("無法點擊下一頁或已無下一頁:", e)
            return False
    
    # 讀取單一課程頁
    def scrape_course_page(self):
        for index, course_url in enumerate(self.course_url_list):
            try:
                self.driver.get(course_url)
                time.sleep(random.uniform(2, 4))
                self.scrape_course_infor()
                print(f"已抓取課程 {index+1}/{len(self.course_url_list)}")
            except Exception as e:
                print(f"第 {index+1} 筆課程失敗: {e}")
                self.error_url_list.append(course_url)

    # 抓取課程資訊
    def scrape_course_infor(self):
        # 無資訊則儲存空值
        def safe_get(selector):
            try:
                return self.driver.find_element(By.CSS_SELECTOR, selector).text
            except:
                return ''
        
        intro_course = ""
        intro_teacher = ""
        intro_notice = ""
        found_tabs = []
        try:
            tabs = self.driver.find_elements(By.CSS_SELECTOR, 'span.nav__direction--text')
            for tab in tabs:
                tab_name = tab.text.strip()
                if tab_name == "課程介紹":
                    tab.click()
                    time.sleep(1)
                    print(f"點擊頁籤: {tab_name}")                    
                    intro_course = safe_get('section.course-video__secondary--content.content--course-intro')
                    found_tabs.append(tab_name)
                elif tab_name == "講師簡介":
                    tab.click()
                    time.sleep(1)
                    print(f"點擊頁籤: {tab_name}")                    
                    intro_teacher = safe_get('section.course-video__secondary--content.content--speaker-intro')
                    found_tabs.append(tab_name)
                elif tab_name == "注意事項":
                    tab.click()
                    time.sleep(1)
                    print(f"點擊頁籤: {tab_name}")                    
                    intro_notice = safe_get('section.course-video__secondary--content.content--noticed-list')
                    found_tabs.append(tab_name)
            # 確認有哪些頁籤沒找到
            target_tabs = ["課程介紹", "講師簡介", "注意事項"]
            missing_tabs = [t for t in target_tabs if t not in found_tabs]
            if missing_tabs:
                print(f"找不到的頁籤: {', '.join(missing_tabs)}")
        except Exception as e:
            print(f"點擊頁籤失敗: {e}")

        # 開始擷取資訊
        course_teacher = safe_get('h4.speaker__name')
        course_type = safe_get('a.tag__icon.tag__icon--orange')
        course_price = safe_get('b.details__item--emphasis')

        self.course_teacher_list.append(course_teacher)
        self.course_type_list.append(course_type)
        self.course_price_list.append(course_price)
        self.intro_course_list.append(intro_course)
        self.intro_teacher_list.append(intro_teacher)
        self.intro_notice_list.append(intro_notice)

        # course_teacher = safe_get('h4.speaker__name')
        # course_type = safe_get('a.tag__icon.tag__icon--orange')
        # course_price = safe_get('b.details__item--emphasis')
        # intro_course = safe_get('section.course-video__secondary--content.content--course-intro')
        # intro_teacher = safe_get('section.course-video__secondary--content.content--speaker-intro')
        # intro_notice = safe_get('section.course-video__secondary--content.content--noticed-list')

    # 儲存檔案
    def save_result(self):
        df = pd.DataFrame({
            '講師資訊': self.course_teacher_list,
            '實體課程': self.course_type_list,
            '課程售價': self.course_price_list,
            '課程介紹': self.intro_course_list,
            '講師簡介': self.intro_teacher_list,
            '注意事項': self.intro_notice_list,
            '課程連結': self.course_url_list
            })
        
        df.to_csv('udn_course_detail.csv', index=False, encoding='utf-8-sig')
        print("已儲存課程詳細資料")


if __name__ == '__main__':
    domain_url = 'https://health.udn.com'
    start_url = 'https://health.udn.com/service/index?cate=全部&from=udn-clubtn6_ch1005'
    scrape = UdnCourseLink(start_url, domain_url)
    start_time = time.time()
    scrape.scrape_all_page()
    end_time = time.time()
    spend_time = round(end_time - start_time, 2)
    print(f'Total Spend Time: {spend_time}')
    print('Job Done!')
