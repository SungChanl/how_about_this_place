from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
url_list = []

landmark = []
review = []
df_total = pd.DataFrame()
df_country = pd.DataFrame
df_city = pd.DataFrame
df_landmark = pd.DataFrame
df_review = pd.DataFrame
for url in range(1, 2):      # 3
    df = pd.read_csv('./crawling_data/crawling_url_{}'.format(url))
    url_list = df['0'].tolist()
    # tourist-attractions/ 이후의 부분을 제거
    cleaned_urls = [url.split('tourist-attractions/')[0] for url in url_list]

    for url_1 in range(30, len(cleaned_urls)):  # cleaned_urls
        page_url = cleaned_urls[url_1] + 'tourist-attractions/comment-count-1011-100'       # cleaned_urls
        # driver.get(page_url)
        # time.sleep(1)
        country = []
        city = []
        cities = None
        count = 30

        for page in range(1, 3):

            try:

                page_url_last = page_url + '/{}.html'.format(page)
                driver.get(page_url_last)
                time.sleep(1)
                countries = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div[1]/div[3]/nav/div[4]/a').text
                # country.append(countries)
                cities = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div[1]/div[3]/nav/div[6]/a').text
                # city.append(cities)
                print(countries, cities)
                landmark_list = driver.find_elements(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div[2]/div/div/div[2]/div[2]/ul/li')
            except:
                continue

            for landmarks in range(10):
                try:
                    _landmarks = landmark_list[landmarks].find_element(By.TAG_NAME, 'a')
                    landmarks_ = _landmarks.get_attribute('title')
                    landmark.append(landmarks_)
                    print(landmark)
                except:
                    continue

                current_window_handle = driver.current_window_handle
                while True:
                    try:
                        landmark_url = driver.find_element(By.XPATH,
                                            '//*[@id="__next"]/div[1]/div[2]/div[2]/div/div/div[2]/div[2]/ul/li[{}]/a/div[5]'
                                            .format(landmarks + 1))
                        landmark_url.click()
                    except ElementClickInterceptedException:
                        continue
                    break

                # time.sleep(2)

                # 모든 창 핸들 가져오기
                all_window_handles = driver.window_handles

                # 새 탭으로 전환
                for handle in all_window_handles:
                    if handle != current_window_handle:
                        driver.switch_to.window(handle)  # 새 탭으로 전환
                        print('switch')
                        break
                while True:
                    try:
                        driver.find_element('xpath', '//*[@id="poi.detail.overview"]/div/div[3]/div[1]/div[1]/div/div[2]/span[2]/div').click()
                    except NoSuchElementException:
                        try:
                            driver.find_element('xpath', '//*[@id="poi.detail.overview"]/div/div/div[1]/div/div[2]/span[2]/div').click()
                        except NoSuchElementException:
                            continue
                    break
                # time.sleep(2)
                collected = None
                review_list = ""
                for review_page in range(29):
                    for reviews in range(1, 6):
                        try:
                            try:
                                reviews_ = driver.find_element(By.XPATH, '//*[@id="reviews"]/div[1]/div/div/div[3]/div[2]/div/ul/div[{}]/li/div[2]/div[2]/a/p'.format(reviews)).text
                            except NoSuchElementException:
                                reviews_ = driver.find_element(By.XPATH, '//*[@id="reviews"]/div[1]/div/div/div[2]/div[2]/div/ul/div[{}]/li/div[2]/div[2]/a/p'.format(reviews)).text
                            refined_review = re.compile('[^가-힣]').sub(' ', reviews_)
                            review_list += refined_review
                            print(refined_review)
                        except:
                            pass

                    while True:  # infinite loop for button click
                        try:
                            next_btn = driver.find_element(By.XPATH,
                                                           '//*[@id="reviews"]/div[1]/div/div/div[3]/div[2]/div/div/div/div/button[2]')
                            next_btn.click()
                        except ElementClickInterceptedException:
                            continue
                        except NoSuchElementException:

                            while True:
                                try:
                                    next_btn1 = driver.find_element(By.XPATH,
                                                                    '//*[@id="reviews"]/div[1]/div/div/div[2]/div[2]/div/div/div/div/button[2]')
                                    next_btn1.click()
                                except ElementClickInterceptedException:
                                    continue
                                except NoSuchElementException:
                                    continue
                                break

                        break
                    time.sleep(1.5)
                driver.close()
                review.append(review_list)
                driver.switch_to.window(current_window_handle)  # 원래 탭으로 전환

                count += 1


            country = [countries]*len(review)
            city = [cities]*len(review)
            df_country = pd.DataFrame(country, columns=['country'])
            # df_city = pd.DataFrame(city, columns=['city'])
            # df_landmark = pd.DataFrame(landmark, columns=['landmark'])
            # df_review = pd.DataFrame(review, columns=['review'])
            df_country['city'] = city
            df_country['landmark'] = landmark
            df_country['review'] = review


        df_total = pd.concat([df_total, df_country], axis='rows', ignore_index=True)

        df_total.to_csv('./crawling_data/review_{}_{}.csv'.format(count, cities), index=False)







