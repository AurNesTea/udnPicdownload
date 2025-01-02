from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

file_path = 'udnWeb\臉書圖卡_文章貼文連結.xlsx -  失智・時空記憶的旅人.csv'
file = pd.read_csv(file_path)
print(file)