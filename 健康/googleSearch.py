import requests
from bs4 import BeautifulSoup
import time, random

my_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

keyword = str(input('請輸入查詢內容'))
gUrl= 'https://www.google.com.tw/search?q='
url = gUrl + keyword

page = 0
eStart = 1
while page <= 1:
    r = requests.get(url, headers=my_headers)
    if r.status_code != 200:
        print(f'status_code: {r.status_code}')
    else:
        print(f'搜尋關鍵字：{keyword}')
        print(f'目前在第 {page+1} 頁')
        soup = BeautifulSoup(r.text, 'html.parser')
        titles = soup.find_all('h3', class_ = 'LC20lb MBeuO DKV0Md')
        links = soup.select('div.yuRUbf')
        # gPages = soup.find_all('a', class_ = 'fl')
        gPages = soup.find('a', id="pnnext")
        
        for idx, (title, link) in enumerate(zip(titles, links), start=eStart):
            title = title.text
            link = link.a.get('href')
            print(f'{idx}: {title}')
            print(link)
            if 'udn.com' in link:
                break
            
        time.sleep(random.randint(1, 3))
        nextPage = gUrl + gPages.get('href').split('/search?q=')[1]
        url = nextPage    
        page += 1
        eStart += 10
