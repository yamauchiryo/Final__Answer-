from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import re
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import codecs

chrome_options = Options()
url = "https://r.gnavi.co.jp/area/aream6202/rs/?date=20240227?p={}"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument('--headless')
url_list = []
link_list = []

#情報の獲得
def get_element_text_class(Class_name):
    try:
        # 要素を見つける
        element = driver.find_element(By.CLASS_NAME, Class_name)
        return element
    except NoSuchElementException:
        return ""
    
#店オフィシャルページの獲得
def get_element_url():
    try:
        element = driver.find_element(By.CLASS_NAME,'sv-of.double').get_attribute('href')
        return element
    except NoSuchElementException:
        # 要素が見つからない場合、空の文字列を返す
        return ""
    
#住所を３つに分割
def parse_address(address):
    pattern = re.compile(r'^(.+?[都道府県])([^\d]+)(\d+.*)$')
    match = pattern.match(address)
    if match:
        prefecture = match.group(1)
        street_name = match.group(2).strip()
        street_number = match.group(3)
        return prefecture, street_name, street_number
    else:
        return None

# 分けたものをそれぞれリストに格納
def address_append(result):
    if result:
        prefecture, street_name, street_number = result
        shop_list.append(prefecture)
        shop_list.append(street_name)
        shop_list.append(street_number)
    else:
        shop_list.append(None)
        shop_list.append(None)
        shop_list.append(None)

# 型によってリストに格納       
def list_append(lst, element):
    try:
        if isinstance(element, str): 
            lst.append(element)
        elif hasattr(element, 'text'):  
            lst.append(element.text)
        else:  # 情報がなければ空を格納する
            lst.append(" ")
    except NoSuchElementException:
        lst.append(" ")
        
# SSL証明書の有無を確認
def check_ssl_certificate(url):
    if url:
        try:
            response = requests.get(url, verify=True)
            T = "True"
            shop_list.append(T)
        except requests.exceptions.SSLError:
            F = "False"
            shop_list.append(F)
    else:
        shop_list.append(" ")
        
#3ページをリストに格納
for i in range(1, 4):
    target_url = url.format(i)
    url_list.append(target_url)
    
#各ページからそれぞれの店ページのURLを取得してリストに格納する
for link in url_list:
    time.sleep(3)  # 3秒間のアイドリング
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    links_elements = driver.find_elements(By.CLASS_NAME, "style_titleLink__oiHVJ")
    # 各要素のhref属性を表示、リストに格納
    for element in links_elements:
        link_list.append(element.get_attribute('href'))
    driver.quit()

link_list_50 = link_list[0:50] #URLを５０個に減らす
df = pd.DataFrame(columns=["店舗名", "電話番号", "メールアドレス", "都道府県", "市区町村", "番地", "建物名", "URL", "SSL"])

#それぞれの情報の取得から格納までをループする
for link in link_list_50:
    time.sleep(3) # 3秒間のアイドリング
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    shop_list = []
    list_append(shop_list,driver.find_element(By.ID, "info-name").text)
    list_append(shop_list,get_element_text_class("number"))
    mail_address = ""
    list_append(shop_list,mail_address)
    address_append(parse_address(driver.find_element(By.CLASS_NAME,"region").text))
    list_append(shop_list,get_element_text_class("locality"))
    list_append(shop_list,get_element_url())
    check_ssl_certificate(get_element_url())
    
    # 文字エンコーディング変更
    shop_list = [codecs.encode(str(element), 'cp932', 'ignore').decode('cp932') for element in shop_list]
    
    df = df._append({"店舗名": shop_list[0],
                    "電話番号": shop_list[1],
                    "メールアドレス": shop_list[2],
                    "都道府県": shop_list[3],
                    "市区町村": shop_list[4],
                    "番地": f'\'{str(shop_list[5])}',
                    "建物名": shop_list[6],
                    "URL": shop_list[7],
                    "SSL": shop_list[8]},
                   ignore_index=True)
    driver.quit()
df.to_csv("1-2.csv", index=False, header=True,encoding="cp932" ,quoting=1)