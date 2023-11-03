from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
import pandas as pd
import re
import time
import datetime

options = Options()
user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 '
              'Safari/537.36')
options.add_argument('user-agent=' + user_agent)
options.add_argument('lang=ko_KR')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')
options.add_argument('--no-sandbox')

with open('./chrome_driver_path.txt', 'r') as f:
    service = Service(executable_path=f.read())

driver = webdriver.Chrome(service=service, options=options)

continent = ['https://kr.trip.com/travel-guide/south-america-120005/',
             'https://kr.trip.com/travel-guide/oceania-120003/',
             'https://kr.trip.com/travel-guide/africa-120006/']

df_URL = pd.DataFrame()
for i in range(2, 3):
    refined_URL = []
    url = continent[i]
    # driver.get(url)
    # time.sleep(1)

    for page in range(1,3):
            for j in range(1, 13):
                try:
                    page_url = url + '{}'.format(page)
                    driver.get(page_url)
                    driver.find_element(By.XPATH,
                                        '//*[@id="__next"]/div[2]/div/div[2]/div[{}]/div/i'.format(j)).click()
                    driver.find_element(By.XPATH,
                                        '//*[@id="travel_guide_root_class"]/div/div[3]/div[1]/a[1]/div[1]/i').click()
                    time.sleep(1)
                    # 현재 탭을 닫고 이전 탭으로 이동
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    current_url = driver.current_url
                    refined_URL.append(current_url)
                    print(refined_URL)
                    time.sleep(1)
                except:
                    print('error{}_{}'.format(page, j))
                    continue
    df_URL = pd.DataFrame(refined_URL)
    df_URL.to_csv('./crawling_data/crawling_url_{}'.format(i), index=False)

