import requests
import time
from bs4 import BeautifulSoup

my_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
urls = [
    'https://www.edh.tw/',
    'https://health.tvbs.com.tw/',
    'https://health.udn.com/health/index'
]
n = 0
e_time = []
t_time = []
u_time = []
while n < 5:
    print(f'第{n+1}次測試')
    for url in urls:
        t1 = time.time()
        r = requests.get(url, headers=my_headers)
        t2 = time.time()
        cost_time = t2-t1
        soup = BeautifulSoup(r.text, 'html.parser')
        print(f'連線至{url}, 共花費 {cost_time} 秒')
        print(soup.text)
        if url == 'https://www.edh.tw/':
            e_time.append(cost_time)
        elif url == 'https://health.tvbs.com.tw/':
            t_time.append(cost_time)
        elif url == 'https://health.udn.com/health/index':
            u_time.append(cost_time)
    n += 1

e_ave = sum(e_time) / len(e_time)
t_ave = sum(t_time) / len(t_time)
u_ave = sum(u_time) / len(u_time)
print(f'連線至早安健康, 平均花費 {e_ave:.4f} 秒')
print(f'連線至健康20, 平均花費 {t_ave:.4f} 秒')
print(f'連線至元氣網, 平均花費 {u_ave:.4f} 秒')