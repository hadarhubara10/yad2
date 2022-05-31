from time import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def get_phone_number():
    driver = webdriver.Chrome(
        'C:\Software Programs\chromedriver_win32\chromedriver.exe')
    driver.get("https://www.yad2.co.il/item/2massij7")
    driver.find_element(By.ID, "lightbox_contact_seller_0").click()
    print(driver.find_element(By.ID, "lightbox_contact_seller_0").text)
    phone_number = driver.find_element(By.CLASS_NAME, "phone_number")
    print(phone_number)


get_phone_number()
