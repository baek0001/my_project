from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pyperclip

driver = webdriver.Chrome(r"C:\Users\Admin\Desktop\chromedriver.exe")
driver.get("https://nid.naver.com/nidlogin.login")

sleep(0.5)
pyperclip.copy('86dnsdyd')
driver.find_element_by_name('id').send_keys(Keys.CONTROL, 'v')

sleep(0.5)
pyperclip.copy('ke3128gz^^')
driver.find_element_by_name('pw').send_keys(Keys.CONTROL, 'v')

driver.find_element_by_xpath('//*[@id="log.login"]').click()
