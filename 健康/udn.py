import requests, re
from bs4 import BeautifulSoup

my_headers = {"user-agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

# 首頁
url = 'https://health.udn.com/health/index'
r = requests.get(url, headers=my_headers)
if r.status_code != 200:
    print(r.status_code)
else:
    headline_title = []
    headline_link = []
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        print('UDN 首頁頭條')
        headlines = soup.find('div', class_ = 'splide__list').find_all('a')
        for headline in headlines:
            print(headline.text)
            print(headline.get('href'))
    
    finally:
        print(headline_title)
        print(headline_link)