from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pyperclip

driver = webdriver.Chrome(r"C:\Users\Admin\Desktop\chromedriver.exe")
driver.get("https://www.schoolinfo.go.kr/")
# driver.get("https://www.schoolinfo.go.kr/ei/ss/pneiss_a05_s0.do")

# driver.find_element_by_css_selector("body > div.school_wrap > header > div > div.gnb_wrap > div > nav > ul > li:nth-child(3) > a").Click();

# driver.find_element_by_xpath("//*[@id="searchForm"]/div/div/div[1]/div/ul/li[3]/label").click();
