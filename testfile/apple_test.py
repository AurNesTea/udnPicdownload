
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import jieba, nltk, time, random

channels = 'https://podcasts.apple.com/tw/podcast/%E6%97%A9%E5%AE%89%E5%81%A5%E5%BA%B7podcast/id1612751706'

options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

try:
    driver.get(channels)
    locator = (By.CLASS_NAME, 'dir-wrapper')
    WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located(locator))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    channel_name = soup.find('h1', class_ = 'headings__title svelte-1scg3f0').text
    btns = driver.find_elements(By.CLASS_NAME, 'svelte-1wtdvjb')
    for btn in btns:
        if '顯示全部' in btn.text:
            btn.click()
            print('已點擊顯示全部按鈕')
        else:
            continue

    time.sleep(2)
    WebDriverWait(driver, 5, 0.5).until(EC.presence_of_all_elements_located)
    
    soup2 = BeautifulSoup(driver.page_source, 'html.parser')
    ep_sections = soup2.find_all('div', class_ = 'section section--episode svelte-1f64bnu')    #   查找所有年份
    print(channel_name)
    
    title_list = []
    if len(ep_sections) < 1:
        print('單一年份')
        ep_year = soup2.find('span', class_ = 'dir-wrapper')
        ep_lists = soup2.find_all('li', class_ = 'svelte-8rlk6b')
        for ep in ep_lists:
            title = ep.find('span', class_ = 'episode-details__title-text')
            print(title.text)
            title_list.append(title.text)
    else:
        print('多個年份')
        for ep_section in ep_sections:
            ep_year = ep_section.find('span', class_ = 'dir-wrapper')
            ep_lists = ep_section.findAll('ol', class_ = 'svelte-8rlk6b')
            for ep in ep_lists:
                titles = ep.findAll('span', class_ = 'episode-details__title-text')
                for title in titles:
                    print(ep_year.text, title.text)
                    title_list.append(title.text)

except Exception as e:
    print(f'Error message: {e}')
finally:
    print('任務完成')
    driver.quit()
