import requests
from bs4 import BeautifulSoup

start_url = 'https://health.udn.com/health/cate/10691/123902'
my_header = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}

r = requests.get(start_url, headers=my_header)
if r.status_code != 200:
    print(r.status_code)
else:
    soup = BeautifulSoup(r.text, 'html.parser')
    print(soup)
    author = soup.find('span', class_ = 'story__content__author')
    content = soup.find('div', class_= 'stroy_text_wrapper').text

    print(author)
    print(content)