import requests
from bs4 import BeautifulSoup
import pandas as pd

my_headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
payLoad = {'share': 'copy'}

url = 'https://health.tvbs.com.tw/'

r = requests.get(url, headers = my_headers) #headers = my_headers, data = payLoad)

if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'html.parser')
    # headline_titles = soup.find_all('h2', class_ = 'pt-2 text-xl line-clamp-2 font-semibold hover:text-[#124008] lg:text-lg xl:text-xl')
    hd_links = soup.find_all('div', class_ = 'flex space-x-6 lg:space-x-4 xl:space-x-6')
    hd_title_list = []
    hd_link_list = []
    hd_editor_list = []
    hd_date_list = []

    # print('<首頁頭條>')
    for link in hd_links:
        links = link.find_all('a')
        for link in links:
            nextlink = link.get('href')

            r2 = requests.get(nextlink, headers = my_headers)
            if r2.status_code == 200:
                soup2 = BeautifulSoup(r2.text, 'html.parser')
                hd_title = soup2.select_one('div.title_box > h1')
                hd_editor = soup2.select_one('div.author_box > li')
                hd_date = soup2.select_one('li.time')

                for title, editor, date in zip(hd_title, hd_editor, hd_date):
                    hd_title_list.append(title.text)
                    hd_link_list.append(nextlink)
                    hd_editor_list.append(editor.text)
                    hd_date_list.append(date.text)
 
    hds = pd.DataFrame({'Title': hd_title_list, 
                        'Links': hd_link_list,
                        'Editor': hd_editor_list,
                        'Date': hd_date_list})

    # print('<首頁文章>')
    frontpage_articles = soup.find_all('a', class_ = 'flex space-x-3 lg:space-x-2 xl:space-x-3')
    catagorys = soup.find_all('div', class_ = 'mb-1 text-sm font-semibold text-[#23812E] md:text-base lg:text-sm xl:text-base')

    for catagory, frontpage_article in zip(catagorys, frontpage_articles):
        print(catagory.text)
        print(frontpage_article.text.split(catagory.text)[1])
        print(frontpage_article.get('href'))
        
        
    # # with pd.ExcelWriter('Health20_headline.xlsx') as writer:
    # #     hds.to_excel(writer,sheet_name='<首頁頭條>', index = False)