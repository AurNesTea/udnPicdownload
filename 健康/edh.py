import requests
from bs4 import BeautifulSoup

my_headers = {"user-agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

'''
首頁大看板
'''
url = 'https://www.edh.tw/'
r = requests.get(url, headers=my_headers)

if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        print('<首頁頭條>')
        headlines = soup.find_all('div', class_='item')
        article_count = 0
        for headline in headlines:
            if article_count >= 12:
                break
            else:
                nextUrl = 'https://www.edh.tw/'+str(headline).split('href="https://www.edh.tw/')[1].split('">')[0].split('"')[0]    
                r_next = requests.get(nextUrl, headers=my_headers)
                
                if r_next.status_code == 200:
                    soup_next = BeautifulSoup(r_next.text, 'html.parser')
                    article_title = soup_next.find('h1', class_ = 'title')
                    date = soup_next.find('span', class_ = 'date')
                    
                    print(article_title.text)
                    print(date.text.split('|')[0])
                    print(nextUrl)
                    print()
                    article_count += 1
    except Exception as e:
        print('網址不正確！',e)
    
    hot_urls = ['https://www.edh.tw/latest/1',
                'https://www.edh.tw/top10/today']
    for hot_url in hot_urls:
        r_hot = requests.get(hot_url)
        soup_hot = BeautifulSoup(r_hot.text, 'html.parser')
        news_titles = soup_hot.find_all('h3', class_ = 'title')
        
        for news_title in news_titles:
            print(news_title.text)
            print('https://www.edh.tw/'+ news_title.a.get('href'))