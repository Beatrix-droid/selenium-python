from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from config import credentials
from datetime import date
from calendar import monthrange

#initialise browser
options = Options()
options.binary_location = '/usr/bin/firefox'
options.headless=True
browser = webdriver.Firefox(options=options)


#check if it is friday or the end of the month:
"""
current_day = date.today()
print(current_day)

if current_day.strftime("%A")== "Friday":
    print("running the crontab")
else:
    print(current_day.strftime("%A"))


if current_day.day==monthrange(current_day.year, current_day.month)[1]:
    print("hello")
print(monthrange(current_day.year, current_day.month), current_day.day)
"""

# go to login portal
browser.get('https://softwareinstitute.bamboohr.com/login.php')

# click 'login' with email and password:

classic_login=browser.find_element(By.CSS_SELECTOR,".fab-link").click()


# identify login form:
email= browser.find_element(By.CSS_SELECTOR, "#lemail")
password=browser.find_element(By.CSS_SELECTOR, "#password")
#type into form
password.send_keys(credentials["password"])
email.send_keys(credentials["username"])

#submit form 
submit_button=browser.find_element(By.XPATH,"//button[@type='submit']")
submit_button.click()
#confirm tp user we have logged in
print("succesfully logged in!")

#locate my "my timesheet" button and click on it
timesheet_link=browser.find_element(By.LINK_TEXT, "My Timesheet").click()

print("opened by time sheet")

    
