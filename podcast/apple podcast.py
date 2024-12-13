from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import jieba, nltk, time
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

def word_Cloud(titles):
    # 下載停用詞
    nltk.download('stopwords', quiet=True)

    # 合併所有標題為一個長字串
    text = " ".join(titles)

    # 使用 jieba 進行中文分詞
    words = jieba.lcut(text, cut_all=False)

    # 去除停用詞
    stop_words = set(stopwords.words('chinese'))    # 選中文詞庫
    filter_word = []
    for word in words:
        if word not in stop_words:
            filter_word.append(word)

    # 計算頻率
    word_freq = Counter(filter_word)

    # 生成文字雲
    word_cloud = WordCloud(font_path='/System/Library/Fonts/STHeiti Medium.ttc',
                        background_color='white',    # 設定底色
                        width=800,       # 設定寬度
                        height=600,      # 設定高度
                        max_words=100    # 設定字數
                        ).generate_from_frequencies(word_freq)

    # 顯示文字雲
    plt.figure(figsize=(10, 8))
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    


def scroll_to_bottom(chrome, delayTime=3, max_scrolls=10):
    last_height = chrome.execute_script("return document.body.scrollHeight")
    scroll_attemps = 0

    while scroll_attemps < max_scrolls:
        # 滾動到頁面底部
        chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delayTime)

        # 計算新的滾動高度
        new_height = chrome.execute_script("return document.body.scrollHeight")
        
        # 如果高度不再變化，表示已經到底部
        if new_height == last_height:
            scroll_attemps += 1
            time.sleep(delayTime)
        else:
            scroll_attemps = 0
        
        last_height = new_height

    print('已到網頁最底部！')

def apple_Podcast(channels):
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
        return title_list

def search_multi_channels(channels):
    # 取得Apple Podcast
    for channel in channels:
        title_list = apple_Podcast(channel)

        # 解析並產生文字雲
        word_Cloud(title_list)
        # time.sleep(random.randint(3))

def check_single_channel(channel):
    title_list = apple_Podcast(channel)

    word_Cloud(title_list)

    
channel = input('請輸入要查詢的Apple Podcast 首頁連結')
check_single_channel(channel)

# channels = ['https://podcasts.apple.com/tw/podcast/%E6%97%A9%E5%AE%89%E5%81%A5%E5%BA%B7podcast/id1612751706',
#             'https://podcasts.apple.com/tw/podcast/%E8%81%BD%E5%BA%B7%E5%81%A5/id1663437331'
#             'https://podcasts.apple.com/tw/podcast/50-talk/id1697436016']
