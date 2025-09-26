import pandas as pd
import requests
from bs4 import BeautifulSoup



def getQA(disease_urls, topic):
    cLink_list = []
    disease_list = []
    main_cate = []
    sub_cate = []
    ques_list = []
    aLink_list = []
    my_header = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
    domain = 'https://health.udn.com'
    for disease_url in disease_urls:
        r = requests.get(disease_url, headers=my_header)
        if r.status_code != 200:
            print(r.status_code)
        else:
            soup = BeautifulSoup(r.text, 'html.parser')
            disease_name = soup.find('h3', class_ = 'care-catalogue__title container__title--shared')
            disease_name = disease_name.text.replace(' ', '').replace('\n', '')
            cates = soup.find('nav', class_ = 'care-catalogue__nav-list')
            cate_links = cates.find_all('a', class_ = 'care-catalogue__nav-item')
            for cate_link in cate_links:
                cate_link = domain + cate_link.get('href').split('?from')[0]
                cLink_list.append([disease_name, cate_link])

    for name, url in cLink_list:
        r = requests.get(url, headers=my_header)
        if r.status_code != 200:
            print(r.status_code)
        else:
            soup = BeautifulSoup(r.text, 'html.parser')
            list_title = soup.find('div', class_ = 'care-catalogue-list__title')
            list_title = list_title.text.replace(' ', '').replace('\n', '')
            groups = soup.find_all('div', class_ = 'care-catalogue-list__group')
            for group in groups:
                sub_name = group.find('h3', class_ = 'care-catalogue-list__item care-catalogue-list__item--title')
                sub_name = sub_name.text.replace(' ', '').replace('\n', '')
                q_list = group.find_all('a', class_ = 'question-list__item')
                for q in q_list:
                    ques = q.text.replace(' ', '').replace('\n', '')
                    link = domain + q.get('href')
                    print(f'疾病:{name}, 類別:{list_title}, 主題:{sub_name}, 問題:{ques}, 解答連結:{link}')
                    disease_list.append(name)
                    main_cate.append(list_title)
                    sub_cate.append(sub_name)
                    ques_list.append(ques)
                    aLink_list.append(link)

    qa_list = pd.DataFrame({'疾病': disease_list,
                            '類別': main_cate,
                            '主題': sub_cate,
                            '問題': ques_list,
                            '解答連結': aLink_list})

    qa_list.to_csv(f'元氣網照護百科_{topic}QA.csv', index=False)

disease_urls = ['https://health.udn.com/health/care/parkinsonsdisease',
                'https://health.udn.com/health/care/dementia']
topic = '失智相關'
getQA(disease_urls, topic)