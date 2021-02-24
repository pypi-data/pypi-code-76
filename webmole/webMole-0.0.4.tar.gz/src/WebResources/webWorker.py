from selenium import webdriver  # for webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
import json

PATH = "src\WebResources\chromedriver.exe"


# HERE TODO:
# Be able to load the html class or id for the title and prince of the product


def startSelenium(path=PATH):
    # option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    driver = webdriver.Chrome(path)
    return driver



def clear_cookies(driver, html_id,html_xpath):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,html_id))).click()
    except:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,html_xpath))).click()


def getData(driver,html_title_class,html_title_Xpath,html_price_class,html_price_Xpath):
        #######
        #GET PRODUCT TITLE AND PRICE

        # HERE WILL BE MADE ALL TRY AND EXCPET SO IT GETS DATA CURRECTLY
        # FIRST IT WILL USE CLASS, IF IT DOENS WORK OR THE RESULT IS AN EMPTY STRING IT WILL SEARCH USING XPATH
        #######

        #GET PRODUCT TITLE(NAME)
        try:
            productTitle = driver.find_element_by_class_name(html_title_class).text

            if productTitle == "":
                productPrice = driver.find_element_by_xpath(html_title_Xpath).text
        except:
            productTitle = driver.find_element_by_xpath(html_title_Xpath).text
        
        #GET PRODUCT PRICE(MONEY)
        try:
            productPrice = driver.find_element_by_class_name(html_price_class).text
            
            if productPrice == "":
                productPrice = driver.find_element_by_xpath(html_price_Xpath).text
        except:
            productPrice = driver.find_element_by_xpath(html_price_Xpath).text
       
       


# TODO
# MAKE SURE ALL WEBSITES WORK, GETTING THE DATA
def getWeb_data(url=None):
    driver = startSelenium()
    driver.get(url)
    shopName = url.split('.')[1]

    with open("src\WebResources\config.json") as File:
        data = json.load(File)
        
        #######
        #FOR COOKIES

        # cookies_id = data["websites"][shopName]["properties"]["cookies"]["html_id"]
        # cookies_xpath = data["websites"][shopName]["properties"]["cookies"]["html_Xpath"]
        # clear_cookies(driver,cookies_id,cookies_xpath)
        #######

        #######
        #GET PRODUCT TITLE AND PRICE

        # HERE WILL BE MADE ALL TRY AND EXCPET SO IT GETS DATA CURRECTLY
        # FIRST IT WILL USE CLASS, IF IT DOENS WORK OR THE RESULT IS AN EMPTY STRING IT WILL SEARCH USING XPATH
        #######

        #GET PRODUCT TITLE(NAME)
        product_title_class = data["websites"][shopName]["properties"]["product_title"]["html_class"]
        product_title_Xpath = data["websites"][shopName]["properties"]["product_title"]["html_Xpath"]

        product_price_class = data["websites"][shopName]["properties"]["product_price"]["html_class"]
        product_price_Xpath = data["websites"][shopName]["properties"]["product_price"]["html_Xpath"]
        
        try:
            productTitle = driver.find_element_by_class_name(product_title_class).text

            if productTitle == "":
                productPrice = driver.find_element_by_xpath(product_title_Xpath).text
        except:
            productTitle = driver.find_element_by_xpath(product_title_Xpath).text
        
        #GET PRODUCT PRICE(MONEY)
        try:
            productPrice = driver.find_element_by_class_name(product_price_class).text
            
            if productPrice == "":
                productPrice = driver.find_element_by_xpath(product_price_Xpath).text
        except:
            productPrice = driver.find_element_by_xpath(product_price_Xpath).text
       
        print(productPrice)
        print(productTitle)
        information_dict = dict(name_product=productTitle,
                                store_product=shopName, 
                                price_product=productPrice)
        
        return information_dict

