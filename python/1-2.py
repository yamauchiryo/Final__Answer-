from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import re
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

url = ["https://r.gnavi.co.jp/rhuymzbd0000/?sc_lid=home_check_shop",
       "https://r.gnavi.co.jp/hx96p6dt0000/",
       "https://r.gnavi.co.jp/farxdmte0000/?rcm_id=10117271020240220203966&sc_dsp=rs-rcm_218743",
       "https://r.gnavi.co.jp/g095628/?rcm_id=00417263020240220552707&sc_lid=r-r_area01_19_5",
       "https://r.gnavi.co.jp/68cskt9c0000/?sc_lid=r-r_history01",
       "https://r.gnavi.co.jp/8apauv4n0000/?sc_type=area&sc_area=jp&sc_dsp=rs_221362",
       "https://r.gnavi.co.jp/cm4fdk670000/?rcm_id=003172525202402201574122",
       "https://r.gnavi.co.jp/g616100/?rcm_id=001172342202402201628449&sc_lid=r-r_area01_19_5",
       "https://r.gnavi.co.jp/k79tc8db0000/?rcm_id=003172525202402201628116",
       "https://r.gnavi.co.jp/gb26400/?rcm_id=10117271020240220532116&sc_lid=rcm01_home_24_3",
       "https://r.gnavi.co.jp/7ymevxpy0000/?sc_lid=home_check_shop",
       "https://r.gnavi.co.jp/6vregz900000/?sc_type=area&sc_area=AREAL2217&sc_dsp=rs_221754&gaphoto=0n6l_2",
       "https://r.gnavi.co.jp/fd2pjtn30000/?sc_dsp=shop_218729",
       "https://r.gnavi.co.jp/r8hcys210000/?sc_type=area&sc_area=PREF13&sc_dsp=rs_219353",
       "https://r.gnavi.co.jp/ej054cpt0000/",
       "https://r.gnavi.co.jp/6vregz900000/?sc_lid=r-r_history01",
       "https://r.gnavi.co.jp/6sjngkk90000/?rcm_id=004172630202402201631489",
       "https://r.gnavi.co.jp/fyt8nfcz0000/?sc_type=area&sc_area=AREAL3701&sc_dsp=rs_223696",
       "https://r.gnavi.co.jp/28zpdzmx0000/",
       "https://r.gnavi.co.jp/6575gxeg0000/",
       "https://r.gnavi.co.jp/5rz6t7yn0000/",
       "https://r.gnavi.co.jp/56rwjb2d0000/",
       "https://r.gnavi.co.jp/brwxhhay0000/",
       "https://r.gnavi.co.jp/fgkz13p20000/?rcm_id=00217250320240221333038",
       "https://r.gnavi.co.jp/2v98kssy0000/?rcm_id=00217250320240221333038",
       "https://r.gnavi.co.jp/8pytk2ey0000/?rcm_id=00217250320240221333038",
       "https://r.gnavi.co.jp/k2880s4r0000/?sc_type=area&sc_area=jp&sc_dsp=rs_223351",
       "https://r.gnavi.co.jp/k514400/?sc_lid=r-r_display01&sc_dsp=shop_222584",
       "https://r.gnavi.co.jp/kak3500/?rcm_id=00417263020240221345561&sc_lid=r-r_area01_19_5",
       "https://r.gnavi.co.jp/3ej3e14b0000/?sc_type=area&sc_area=PREF01&sc_dsp=rs_222187",
       "https://r.gnavi.co.jp/5sajrf0c0000/?rcm_id=00117234220240221346360",
       "https://r.gnavi.co.jp/h642700/?rcm_id=00117234220240221346649&sc_lid=r-r_area01_19_5",
       "https://r.gnavi.co.jp/ad96xd5y0000/",
       "https://r.gnavi.co.jp/6k93par80000/?rcm_id=00117234220240221347266",
       "https://r.gnavi.co.jp/3t3t5eg70000/?rcm_id=00317252520240221347545",
       "https://r.gnavi.co.jp/d3asu2ge0000/?sc_dsp=shop_222268",
       "https://r.gnavi.co.jp/k536901/?rcm_id=00217250320240221344229&sc_lid=r-r_area01_19_5",
       "https://r.gnavi.co.jp/120fntjb0000/",
       "https://r.gnavi.co.jp/kak6700/",
       "https://r.gnavi.co.jp/65fr53re0000/?sc_dsp=shop_223335",
       "https://r.gnavi.co.jp/pfww684y0000/?rcm_id=00117234220240221352847",
       "https://r.gnavi.co.jp/7y59rt680000/",
       "https://r.gnavi.co.jp/k170059/",
       "https://r.gnavi.co.jp/ncn0sg740000/",
       "https://r.gnavi.co.jp/k021721/?rcm_id=00117234220240221354595&sc_lid=r-r_area01_19_5",
       "https://r.gnavi.co.jp/k742128/?sc_lid=r-r_display01&sc_dsp=shop_222637",
       "https://r.gnavi.co.jp/r8g5dbjb0000/?rcm_id=00217250320240221354619",
       "https://r.gnavi.co.jp/sryth5az0000/?sc_dsp=shop_223739",
       "https://r.gnavi.co.jp/k742178/?rcm_id=00317252520240221355520&sc_lid=r-r_area01_19_5",
       "https://r.gnavi.co.jp/c604570/?rcm_id=00317252520240221355887&sc_lid=r-r_area01_19_5",
       ]

#都道府県、その後の文字列、その後の数字で分ける
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
#分けたものをそれぞれリストに格納
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
 
#型によってリストに格納       
def list_append(lst, element):
    if isinstance(element, str): 
        lst.append(element)
    elif hasattr(element, 'text'):  
        lst.append(element.text)
    else:#情報がなければ空を格納する
        lst.append(" ")

#SSL証明書の有無を確認
def check_ssl_certificate(url):
    try:
        response = requests.get(url, verify=True)
        T = "True"
        shop_list.append(T)
        return shop_list
    except requests.exceptions.SSLError:
        F = "False"
        shop_list.append(F)
        return shop_list
    
df = pd.DataFrame(columns=["店舗名", "電話番号", "メールアドレス", "都道府県", "市区町村", "番地", "建物名", "URL", "SSL"])

for link in url:
    driver = webdriver.Chrome()
    time.sleep(3)
    driver.get(link)
    shop_name_element = driver.find_element(By.ID, "info-name")
    tele_number_element = driver.find_element(By.CLASS_NAME,"number")
    mail_address = None
    address_element = driver.find_element(By.CLASS_NAME,"region").text

    official_page_link_element = driver.find_element(By.CLASS_NAME,'sv-of.double').get_attribute('href')

    shop_list = []
    list_append(shop_list,shop_name_element)
    list_append(shop_list,tele_number_element)
    list_append(shop_list,mail_address)
    result = parse_address(address_element)
    address_append(result)
    
    try:
        # 要素を見つける
        building_element = driver.find_element(By.CLASS_NAME, "locality")
        
        # 要素が見つかった場合、テキストを取得してリストに追加
        shop_list.append(building_element.text)

    except NoSuchElementException:
    # 要素が見つからない場合、空のリストを追加
        shop_list.append("")
    list_append(shop_list,official_page_link_element)
    ssl_certificate_status = check_ssl_certificate(official_page_link_element)

    df = df._append({"店舗名": shop_list[0],
                    "電話番号": shop_list[1],
                    "メールアドレス": shop_list[2],
                    "都道府県": shop_list[3],
                    "市区町村": shop_list[4],
                    "番地": shop_list[5],
                    "建物名": shop_list[6],
                    "URL": shop_list[7],
                    "SSL": shop_list[8]},
                   ignore_index=True)
    driver.quit()
df.index = range(2, len(df)+2)
df.to_csv("1-2.csv", index_label='1', header=True)
