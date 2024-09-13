import time
from time import sleep
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

URL = "https://map.naver.com/v5/search/"
CHROMEDRIVERPATH = "/usr/bin/chromedriver"

def initSelenium(executable_path):
    options = Options()
    options.add_argument('--headless')
    #options.add_argument('--window-size=1920x1080')
    #options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    service = Service(executable_path=executable_path)
    return webdriver.Chrome(service=service, options=options)

def gotoNaverPlace_entryIframe(driver: webdriver.Chrome):
    driver.implicitly_wait(10)
    try:
        driver.switch_to.frame(driver.find_element(By.ID, "entryIframe"))
    except NoSuchElementException:
        driver.switch_to.frame(driver.find_element(By.ID, "searchIframe"))

        try:
            driver.find_element(By.CSS_SELECTOR, "#_pcmap_list_scroll_container > ul > li:nth-child(1) > div:nth-child(1) > a").click()
        except NoSuchElementException:
            try:
                driver.find_element(By.CSS_SELECTOR, "#_pcmap_list_scroll_container > ul > li:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)").click()
            except NoSuchElementException:
                try:
                    driver.find_element(By.CSS_SELECTOR, "#_pcmap_list_scroll_container > ul > li:nth-child(1) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)").click()
                except NoSuchElementException:
                    return False

        driver.switch_to.default_content()
        try:
            driver.switch_to.frame(driver.find_element(By.ID, "entryIframe"))
        except NoSuchElementException:
            driver.find_element(By.CSS_SELECTOR, "#section_content > div > div:nth-child(3) > div")
            try:
                driver.switch_to.frame(driver.find_element(By.ID, "entryIframe"))
            except NoSuchElementException:
                return False
        return True

def switchToMenuTabInNaverPlace(driver):
    tabs = driver.find_elements(By.CSS_SELECTOR, 'div.place_fixed_maintab > div > div > div > div > a')

    for tab in tabs:
        cursor = tab.find_element(By.TAG_NAME, 'span').get_attribute("innerHTML")

        if (cursor != "메뉴"): continue
        tab.click()
        return True
    return False

def getMenusOnNaverOrder(driver):
    preProcessMenus = driver.find_elements(By.CLASS_NAME, "tit")

    menuText = set()

    for item in preProcessMenus:
        menuText.add(item.get_attribute("innerText"))

    menuText.discard("대표")

    return menuText

def getMenusOnNaverPlace(driver):
    preProcessMenus = driver.find_element(By.CSS_SELECTOR, '.place_section_content').find_elements(By.TAG_NAME, "span")

    menuText = set()

    for item in preProcessMenus:
        menuText.add(item.get_attribute("innerText"))

    menuText.discard("대표")

    return menuText

def getMenusByName(name):
    driver = initSelenium(CHROMEDRIVERPATH)

    driver.get(URL + name)

    if gotoNaverPlace_entryIframe(driver) == False:
        return ["No such restaurant"]
    if switchToMenuTabInNaverPlace(driver) == False:
        return ["This restaurant has no menu data"]
        
    title = driver.find_element(By.XPATH, "/html/head/title")
    if title.get_attribute("innerHTML") != "네이버 플레이스":
        return getMenusOnNaverOrder(driver)
    else:
        return getMenusOnNaverPlace(driver)

if __name__ == '__main__':
    I = 0
    for menu in getMenusByName(input("식당 이름 입력: ")):
        print('<?' + str(I) + '?>' + menu)
        I+=1