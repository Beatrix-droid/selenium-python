from config import credentials
from helium import *
from datetime import date
from calendar import monthrange

from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
#initialise browser




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

#initialise browser
options= FirefoxOptions()
browser=start_firefox('https://softwareinstitute.bamboohr.com/login.php', options=options, headless=True)

# click 'login with email and password':
click("Log in with Email and Password")



#type into login form and submit form:
# identify login form:
email= browser.find_element(By.CSS_SELECTOR, "#lemail")
password=browser.find_element(By.CSS_SELECTOR, "#password")
#type into form
password.send_keys(credentials["password"])
email.send_keys(credentials["username"])

click("Log In")

# confirm to user we have logged in
title=browser.find_element(By.TAG_NAME, "span")
print(title.text)
print("succesfully logged in!")

# locate my "my timesheet" button and click on it
click("My Timesheet")
# confirm that the timesheet was opened
assert Text("Timesheet").exists()
print("opened by time sheet")


#begin filling in the work hours
week=["Mon", "Tue", "Wed", "Thur", "Fri"]
for day in week:
    click(day)
    click("Add Time Entry")
    if Text("Day Total: 7h 30m").exists() or Text("Day Total: 8h").exists() :
        click("Cancel")  # if there are alreaddy hrs logged in skip
    
    else:   # log the hours and click save
        write("7.5")
        click("--Select Project/Task--")
        click("Liberty Global Automation & AI")
        click("Save")
        # confirm that we are back to the timesheet page
        assert Text("Timesheet").exists()
