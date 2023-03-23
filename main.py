from config import credentials

from datetime import date
from calendar import monthrange
from selenium import webdriver
from helium import *
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

# initialise browser


# check if it is friday or the end of the month:
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


# configure the options for the browser
options = Options()
options.binary_location = "/usr/bin/firefox"
options.add_argument("--headless")


# initialise an instance of the browser
browser = start_firefox(options=options)


# navigate to the login page
browser.get("https://softwareinstitute.bamboohr.com/login.php")


# check if login page has loaded correctly
spans = browser.find_elements(By.TAG_NAME, "span")
text_spans = [span.text for span in spans]

page_has_loaded = bool("Log in with SAML" in text_spans)
assert page_has_loaded == True, "Error page not loaded correctly"

if page_has_loaded==False:
   browser.save_screenshot("login_page.png")


# click 'login with email and password':
click("Log in with Email and Password")

# identify login form and check that it has loaded correctly:
email = browser.find_element(By.CSS_SELECTOR, "#lemail")
password = browser.find_element(By.CSS_SELECTOR, "#password")
submit_button=browser.find_element(By.XPATH,"//span[text()='Log In']")

assert submit_button and  password and email, "Error page not loaded correctly"
if submit_button==False or email==False or password==False:
    browser.save_screenshot("no_submit_btn.png")

# type into form
email.send_keys(credentials["username"])
password.send_keys(credentials["password"])

# Submit form
submit_button.click()
# content = driver.find_element(By.CSS_SELECTOR, 'p.content')  to locate by class

browser.save_screenshot("image.png")
# confirm to user we have logged in
links = browser.find_element(By.CLASS_NAME, "MyInfoWidget__title")


#print(Text("My Time").exists())
#print("succesfully logged in!")

# locate my "my timesheet" button and click on it
#click("My Timesheet")
# confirm that the timesheet was opened
#assert Text("Timesheet").exists()
#print("opened by time sheet")


# begin filling in the work hours
week = ["Mon", "Tue", "Wed", "Thur", "Fri"]
for day in week:
    click(day)
    click("Add Time Entry")
    if Text("Day Total: 7h 30m").exists() or Text("Day Total: 8h").exists():
        click("Cancel")  # if there are alreaddy hrs logged in skip

    else:  # log the hours and click save
        write("7.5")
        click("--Select Project/Task--")
        click("Liberty Global Automation & AI")
        click("Save")
        # confirm that we are back to the timesheet page
        assert Text("Timesheet").exists()
