import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random

def getTags(urls, my_header):
    tag_list = []
    count = 0
    for url in urls:
        if count / 100 == 0:
                print('目前已取得{count}則文章的Tag')
                
        r = requests.get(url, headers=my_header)
        if r.status_code != 200:
            print(r.status_code)
        else:
            soup = BeautifulSoup(r.text, 'html.parser')
            print(f'current url: {url}')
            tags = soup.find_all('a', class_ = 'btn-keyword--green')
            for tag in tags:
                tag_list.append(tag.text)
        count += 1
        time.sleep(random.randint(3))
    return tag_list

def getInfors(url, my_header,tag):
    articleTitle_list = []
    articleLink_list = []
    searchTag_list = []
    count = 0

    search_tag = f'失智症+{tag}'
    while True:
        try:
            r = requests.get(url, headers=my_header)
            if r.status_code != 200:
                print(f"Error: HTTP {r.status_code}")
                break
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            break

        soup = BeautifulSoup(r.text, 'html.parser')
        print(f'current search url: {url}')

        articles = soup.find_all('li', class_ = 'item-listing__photo-8to5 pic-8to5-item__wrapper')
        next_page = soup.find('a', class_ = 'pagenation__link pagenation__link--next-page')

        for article in articles:
            link = article.find('a', class_='pic-8to5-item__substance')
            title = article.find('h2', class_='pic-8to5-item__title')
            if link and title:
                articleTitle_list.append(title.text.strip())
                articleLink_list.append(link.get('href').split('?from')[0])
                searchTag_list.append(search_tag)

        count += len(articles)
        if count / 100 == 0:
            print(f'目前已取得{count}則文章的資訊')
        
        time.sleep(random.randint(1, 3))

        if not next_page:
            break
        else:
            url = next_page.get('href')
            if not url.startswith('http'):
                url = f"https://health.udn.com{url}"

    infors = pd.DataFrame({'搜尋TAG': search_tag,
                           '標題': articleTitle_list,
                           '連結': articleLink_list})
    return infors


my_header = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}

tag_file = pd.read_csv('/Users/kevintsai/Library/CloudStorage/OneDrive-個人/Kevin/UDN/程式碼/udnWeb/word_counts.csv')
infor_data = pd.DataFrame()
for tag, count in zip(tag_file['Word'], tag_file['Count']):
    if count <= 2 or tag == '失智症':
        continue
    
    search_url = f'https://health.udn.com/health/search/失智症%20{tag}'
    
    infors = getInfors(search_url, my_header, tag)
    
    if infor_data.empty:
        infor_data = infors
    else:
        infor_data = pd.concat([infor_data, infors], ignore_index=True) 

print(infor_data)
infor_data.to_csv('tag_articles.csv', index=False)

# file = pd.read_csv('/Users/kevintsai/Library/CloudStorage/OneDrive-個人/Kevin/UDN/AI健腦工具/data/失智專區20240910.xlsx - 失智專區.csv')
# urls = file['Link']
# tag_list = getTags(urls)
# print(tag_list)

