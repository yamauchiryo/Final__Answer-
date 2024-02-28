import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd
import codecs

url = "https://r.gnavi.co.jp/area/aream6202/rs/?date=20240227?p={}"
headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
url_list = []
link_list = []

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
    if isinstance(element, str): 
        lst.append(element)
    elif hasattr(element, 'text'):  
        lst.append(element.text)
    else:  # 情報がなければ空を格納する
        lst.append(" ")

# SSL証明書の有無を確認
def check_ssl_certificate(url):
    if url:
        try:
            response = requests.get(url, verify=True)
            return  "True"
        except requests.exceptions.SSLError:
            return "False"
    else:
        return " "

#3ページをリストに格納
for i in range(1, 4):
    target_url = url.format(i)
    url_list.append(target_url)
    
#各ページからそれぞれの店ページのURLを取得してリストに格納する
for link in url_list:
    time.sleep(3)  # 3秒間のアイドリング
    res = requests.get(link, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")
    # 'a' 要素を全て取得
    links = soup.find_all('a', attrs={"class": "style_titleLink__oiHVJ"})
    # 各 'a' 要素の 'href' 属性を取得
    for link_element in links:
        link_list.append(link_element.get('href'))

link_list_50 = link_list[0:50] #URLを５０個に減らす
df = pd.DataFrame(columns=["店舗名", "電話番号", "メールアドレス", "都道府県", "市区町村", "番地", "建物名", "URL", "SSL"])

#それぞれの情報の取得から格納までをループする
for link in link_list_50:
    time.sleep(3)
    res = requests.get(link, headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")
    shop_list = []
    mail_address = None
    official_page_link_element = soup.find('a', attrs={'class': 'sv-of double', 'title': 'オフィシャルページ'})
    
    list_append(shop_list, (soup.find("p", attrs={"class": "fn org summary"})))
    list_append(shop_list, (soup.find("span", attrs={"class": "number"})))
    list_append(shop_list, mail_address)
    address_append(parse_address((soup.find("span", attrs={"class": "region"}).text)))
    list_append(shop_list, (soup.find("span", attrs={"class": "locality"})))
    list_append(shop_list, official_page_link_element.get('href') if official_page_link_element else " ")
    list_append(shop_list, check_ssl_certificate(official_page_link_element.get('href')) if official_page_link_element else " ")

    # 文字エンコーディング変更
    shop_list = [codecs.encode(str(element), 'cp932', 'ignore').decode('cp932') for element in shop_list]

    df = df._append({"店舗名": shop_list[0],
                     "電話番号": shop_list[1],
                     "メールアドレス": shop_list[2],
                     "都道府県": shop_list[3],
                     "市区町村": shop_list[4],
                     "番地": f'="{str(shop_list[5])}"',
                     "建物名": shop_list[6],
                     "URL": shop_list[7],
                     "SSL": shop_list[8]},
                    ignore_index=True)
df.to_csv("1-1.csv", index=False, header=True,encoding="cp932" ,quoting=1)




