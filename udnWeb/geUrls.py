import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://health.udn.com'
start_url = 'https://health.udn.com/health/cate/10691/123902'
my_header = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}

def getTags(start_url, my_header, url):
    tag_list = []
    r = requests.get(start_url, headers=my_header)
    if r.status_code != 200:
        print(r.status_code)
    else:
        soup = BeautifulSoup(r.text, 'html.parser')
        links = soup.find_all('a', class_ = 'pic-8to5-item__substance')
        for link in links:
            # print(link.get('href'))
            new_url = url + link.get('href')
            r2 = requests.get(new_url)
            if r2.status_code != 200:
                print(r2.status_code)
            else:
                print(f'current url: {new_url}')
                soup2 = BeautifulSoup(r2.text, 'html.parser')
                tags = soup2.find_all('a', class_ = 'btn-keyword--green')
                for tag in tags:
                    tag_list.append(tag.text)
    return tag_list
    
tag_list = getTags(start_url, my_header, url)
print(tag_list)
tag_set = set(tag_list)
print(tag_set)
with open('tag_list.txt', mode='w',encoding='utf-8') as f:
    for tag in tag_set:
        f.write(f'{tag}, ')
        