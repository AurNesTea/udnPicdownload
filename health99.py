import pandas as pd
import requests
from bs4 import BeautifulSoup
import time, random


health99_url = 'https://health99.hpa.gov.tw'
def getHealth99(url, my_header):
    title_list = []
    link_list = []
    picLink_list = []
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
        articleLinks = soup.find_all('a', class_ = 'news_list')
        pages = soup.find_all('li', class_ = 'page-item')

        for link in articleLinks:
            link = link.get('href')
            r2 = requests.get(link, headers=my_header)
            if r2.status_code != 200:
                print(f"Error: HTTP {r.status_code}")
            else:
                soup2 = BeautifulSoup(r2.text, 'html.parser')
                title = soup2.find('h2', class_ = 'text-left color_dark_g h3')
                if title == None:
                    continue
                else:
                    pics = soup2.find_all('img')
                    pic = health99_url + pics[5].get('src')
                    print(title.text)
                    print(pic)
                    title_list.append(title.text)
                    link_list.append(link)
                    picLink_list.append(pic)

            time.sleep(random.randint(1, 3))    # snap for request next aritcle link

        if 'disabled' in pages[-1]:
            print('No more next page')
            break
        else:
            url = pages[-1].a.get('href')
            print('get next page')
            

    infors = pd.DataFrame({'文章標題': title_list,
                           '文章連結': link_list,
                           '圖片連結': picLink_list})
    return infors



my_header = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}

infor_data = pd.DataFrame()
keyword_list = ['冠心病', '腦中風', '糖尿病', '高血壓', '心血管不良事件']
for keyword in keyword_list:
    search_url = f'https://health99.hpa.gov.tw/search?keyword={keyword}'
    infors = getHealth99(search_url, my_header)

    if infor_data.empty:
        infor_data = infors
    else:
        infor_data = pd.concat([infor_data, infors], ignore_index=True) 

# save data
infor_data.to_csv('tag_articles.csv', index=False)
