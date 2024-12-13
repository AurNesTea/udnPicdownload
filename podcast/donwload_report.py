from bs4 import BeautifulSoup
import pandas as pd
from adpw import K
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, random

start_url = 'https://host.soundon.fm/auth/login?path=%2Fapp%2Fpodcasts'

options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

try:
    # Login
    driver.get(start_url)
    locator = (By.CLASS_NAME, 'so-login-page__submit')
    WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located(locator))
    driver.find_element(By.ID, 'login-form_email').send_keys(K.sound_ac)
    time.sleep(random.randint(1, 3))
    driver.find_element(By.ID, 'login-form_password').send_keys(K.sound_pw)
    time.sleep(random.randint(1, 3))
    driver.find_element(By.CLASS_NAME, 'so-login-page__submit').click()

    # welcome page
    locator2 = (By.CLASS_NAME, 'ant-select-selection-item')
    WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located(locator2))
    time.sleep(5)
    driver.find_element(By.CLASS_NAME, 'ant-list-item-meta-title').click()
    time.sleep(random.randint(5, 7))
    
    # Dashboard page
    driver.find_elements(By.CLASS_NAME, 'ant-menu-title-content')[5].click()
    time.sleep(random.randint(4, 6))

    # Single Ep
    locator3 = (By.CLASS_NAME, 'app-markdown')
    WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located(locator3))
    # soup_ep = BeautifulSoup(driver.page_source, 'html.parser')
    # ep_table = soup_ep.find('div', class_ = 'ant-table-content')
    # eps = ep_table.find_all('div', class_ = 'ant-space-item')
    time.sleep(random.randint())
    eps = driver.find_elements(By.CLASS_NAME, 'ant-space-item')
    for ep in eps:
        print(ep)
        
    
    # time.sleep(random.randint(1, 4))

    # download Ep overview Repoert
    # driver.find_element(By.CLASS_NAME, 'ant-btn-primary').click()



except Exception as e:
        print(f'Error message: {e}')

finally:
    driver.quit()

