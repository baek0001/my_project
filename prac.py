from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyautogui
from time import sleep
from selenium.webdriver.chrome.options import Options

usr = 'baek0001@gmail.com'
pwd = 'ke3128gz^^'

path = r"C:\Users\Admin\Desktop\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get("http://www.facebook.com")

assert "Facebook" in driver.title

elem = driver.find_element_by_id("email")
elem.send_keys(usr)
elem = driver.find_element_by_id("pass")
elem.send_keys(pwd)
elem.send_keys(Keys.RETURN)

sleep(11.0)

# 알림창 끄기
driver.switch_to.alert.dismiss()