from config import credentials

from datetime import date
from calendar import monthrange
from selenium import webdriver

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
browser = webdriver.Firefox(options=options)



# navigate to the login page
browser.get("https://softwareinstitute.bamboohr.com/login.php")


# check if login page has loaded correctly
spans = browser.find_elements(By.TAG_NAME, "span")
text_spans = [span.text for span in spans]

page_has_loaded = bool("Log in with SAML" in text_spans)

if page_has_loaded == False:
    browser.save_screenshot("login_page.png")
assert page_has_loaded == True, "Error page not loaded correctly"


# click 'login with email and password':
normal_login_button = browser.find_element(
    By.XPATH, "//button[contains(text(),'Log in with Email and Password')]"
).click()
# identify login form and check that it has loaded correctly:
email = browser.find_element(By.CSS_SELECTOR, "#lemail")
password = browser.find_element(By.CSS_SELECTOR, "#password")
submit_button = browser.find_element(By.XPATH, "//span[text()='Log In']")

if submit_button == False or email == False or password == False:
    browser.save_screenshot("no_submit_btn.png")
assert submit_button and password and email, "Error page not loaded correctly"


# type into form
email.send_keys(credentials["username"])
password.send_keys(credentials["password"])


# Submit form
submit_button.click()
# content = driver.find_element(By.CSS_SELECTOR, 'p.content')  to locate by class


# confirm to user we have logged in
my_name = browser.find_element(By.XPATH, "//span[text()='Beatrice Federici']")

if my_name == False:
    browser.save_screenshot("home_page_not_found.png")
assert my_name, " homepage not loaded correctly"

# locate my "my timesheet" button and click on it
my_timesheet = browser.find_element(By.LINK_TEXT, "My Timesheet")
my_timesheet.click()

browser.session_id
# check that we have navigated to the timesheet page:
h3_tags = browser.find_elements(By.TAG_NAME, "h3")

h3_text = [tag.text for tag in h3_tags]
if "Timesheet" not in h3_text:
    browser.save_screenshot("timesheet_not_found.png")
assert "Timesheet" in h3_text, "timesheet page not found"


# click on the time entries
time_sheet_form = browser.find_element(By.TAG_NAME, "form")

#this will be for link in links, but it ammounts to finding the "add time entry" link
link=time_sheet_form.find_element(By.TAG_NAME, "a")
link.click()
browser.save_full_page_screenshot("enter time.png")

#check all the divs, if hrous worked is 7 30m close and do not fill in the sheet
divs= browser.find_elements(By.CLASS_NAME, "div")

div_texts=[div.text for div in divs]
print(div_texts)
#hours=browser.find_element(By.XPATH, "//div[text()='Day Total: 7h 30m']")

#print(bool(hours))

# begin filling in the work hours
week = ["Mon", "Tue", "Wed", "Thur", "Fri"]
# for day in week:
# click the day you need to fill in:
# browser.find_element(By.XPATH, f"//span[text()='{day}']")
#   click("Add Time Entry")
#  if Text("Day Total: 7h 30m").exists() or Text("Day Total: 8h").exists():
#     click("Cancel")  # if there are alreaddy hrs logged in skip
#/html/body/div[3]/section/div[2]/div[2]/div/div[3]/div[1]/form/div[4]/div[2]/div/div[1]/a
# else:  # log the hours and click save
#  write("7.5")
#   click("--Select Project/Task--")
# click("Liberty Global Automation & AI")
# click("Save")
# confirm that we are back to the timesheet page
# assert Text("Timesheet").exists()
