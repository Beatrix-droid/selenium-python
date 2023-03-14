from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from config import credentials
from datetime import datetime

#initialise browser
options = Options()
options.binary_location = '/usr/bin/firefox'
options.headless=True
browser = webdriver.Firefox(options=options)


#check if it is friday or the end of the month:

today = date.today()
print(today)
# go to login portal
browser.get('https://softwareinstitute.bamboohr.com/login.php')
js-normalLoginLink
# click 'login' with email and password:
buttons=driver.find_element(By.TAG_NAME, 'button')
button=buttons.find_element(By.ClASS_NAME, "js-normalLoginLink").click()


# type in username and password:
inputs=driver.find_element(By.TAG_NAME, "input")
email= inputs.find_element().send_keys(credentials["username"])