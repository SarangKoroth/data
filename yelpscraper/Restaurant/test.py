from requests import get
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome('/usr/local/bin/chromedriver',chrome_options=chrome_options)
driver = webdriver.Chrome('/home/dhruv034/Desktop/codemarket/chromedriver_linux64/chromedriver',chrome_options=chrome_options)
#driver = webdriver.Chrome('E:/Codes/chromedriver.exe')#,chrome_options=chrome_options)

url = "https://www.yelp.com/search?find_desc=Indian+food&find_loc=Redondo+Beach%2C+CA"
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_link_text('Start Order')).click()

rest_list = soup.find('ul',class_="undefined list__09f24__17TsU")
lilist = rest_list.findChildren(['li'])
# Explicit wait for the site to load for slow internet connection
wait = WebDriverWait(driver, 20)
# print(lilist)
for li in lilist:
    link = li.find('a',class_="link__09f24__1kwXV link-color--inherit__09f24__3PYlA link-size--inherit__09f24__2Uj95")
    
    if link == None:
        continue
    
    driver.get("https://yelp.com/" + link['href'])
    # wait.until(
    #     lambda driver: driver.find_element_by_class_name('lemon--div__373c0__1mboc tabLabel__373c0__2-upa')
    # ).click()
    rest = driver.page_source
    rest_soup = BeautifulSoup(rest, 'html.parser')
    rest_name = rest_soup.find('h1',class_ = "lemon--h1__373c0__2ZHSL heading--h1__373c0__dvYgw undefined heading--inline__373c0__10ozy").text
    print(rest_name)
    tab = wait.until(EC.element_to_be_clickable((
        By.XPATH, '//div[@class="lemon--div__373c0__1mboc tab__373c0__24QGW tabNavItem__373c0__3X-YR tab--section__373c0__3V0A9 tab--no-outline__373c0__3adQG"]'
    )))
    tab.click()
    order = wait.until(EC.element_to_be_clickable((
        By.XPATH, '//button[@class="button__373c0__3lYgT primary__373c0__2ZWOb full__373c0__1AgIz"]'
    )))
    order.click()
    # wait.until(
    #     lambda driver: driver.find_element_by_link_text("Start Order")
    # ).click()

    time.sleep(10)
    menu_link = driver.current_url
    driver.get(menu_link)
    menu_page = driver.page_source
    menu_soup = BeautifulSoup(menu_page, 'html.parser')
    # print(menu_soup)
    # menu = menu_soup.find('a',class_="lemon--a__85e3c__IEZFH link__85e3c__29943 link-color--blue-dark__85e3c__1mhJo link-size--default__85e3c__1skgq").text
    # print(menu + "Menu")
    # menu_list = menu_soup.find('div',class_="lemon--div__85e3c__1mboc menu-item-wrapper__85e3c__2jk74 u-sm-space-t0 u-sm-space-b0 border-color--default__85e3c__2oFDT")
    # list_menu = menu_list.findChildren(['p'])
    # print(list_menu)

    lm = []
    for data in menu_soup:
        dataframe = {}
        # dataframe["item_name"] = data.find('p',class_="lemon--p__85e3c__3Qnnj text__85e3c__2pB8f name__85e3c__1xq7V text-color--normal__85e3c__K_MKN text-align--left__85e3c__2pnx_").text
        dataframe["price"] = data.find('p',class_="lemon--p__85e3c__3Qnnj text__85e3c__2pB8f price__85e3c__33BRs text-color--normal__85e3c__K_MKN text-align--left__85e3c__2pnx_ text-weight--bold__85e3c__3HYJa").text
        lm.append(dataframe)
    print(lm)