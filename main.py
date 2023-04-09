from calendar import monthrange
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import logging



logging.basicConfig(level=logging.DEBUG)

USER_NAME = os.environ.get("USERNAME")
USER_PASSWORD = os.environ.get("PASSWORD")

# initialise browser
# wait.until(ExpectedConditions.elementToBeClickable(By.id("Login")));

# check if it is friday or the end of the month:
print("starting the automation job")
current_day = date.today()

# check that its friday or the last day of the month
# if (current_day.strftime("%A")== "Friday") or (current_day.day==monthrange(current_day.year, current_day.month)[1]) :
print("filling in the time sheet")


# configure the browser driver
options = FirefoxOptions()
options.add_argument("--headless")
options.add_argument("start-maximized")
options.binary = FirefoxBinary("/usr/bin/firefox")

firefox_service=FirefoxService(GeckoDriverManager().install())





# initialise an instance of the browser

browser = webdriver.Firefox(service=firefox_service, options=options)


# navigate to the login page
browser.get("https://softwareinstitute.bamboohr.com/login.php")


# check if login page has loaded correctly
spans = browser.find_elements(By.TAG_NAME, "span")
text_spans = [span.text for span in spans]

page_has_loaded = bool("Log in with SAML" in text_spans)

assert (
    page_has_loaded
), "Error initial login page not loaded correctly" and browser.save_screenshot(
    "login_page.png"
)


# click 'login with email and password':
normal_login_button = browser.find_element(
    By.XPATH, "//button[contains(text(),'Log in with Email and Password')]"
).click()

# identify login form and check that it has loaded correctly:
email = browser.find_element(By.CSS_SELECTOR, "#lemail")
password = browser.find_element(By.CSS_SELECTOR, "#password")
submit_button = browser.find_element(By.XPATH, "//span[text()='Log In']")

assert (
    submit_button and password and email
), "Error login form not loaded correctly" and browser.save_screenshot(
    "no_submit_btn.png"
)


# type into form
email.send_keys(USER_NAME)
password.send_keys(USER_PASSWORD)

# Submit form
submit_button.click()

# content = driver.find_element(By.CSS_SELECTOR, 'p.content')  to locate by class
my_name=WebDriverWait(browser, 5).until(EC.presence_of_element_located(( By.XPATH, "//span[text()='Graduate Technical Consultant']")))

assert my_name, " homepage not loaded correctly" and browser.save_screenshot(
    "home_page_not_found.png"
)

# locate my "my timesheet" button and click on it
my_timesheet = browser.find_element(By.LINK_TEXT, "My Timesheet")
my_timesheet.click()



# check that we have navigated to the timesheet page:
h3_tags=WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
if browser is None:
    browser.quit()
    print("session got disconnected")

# quit if session is not valid any more

h3_text = [tag.text for tag in h3_tags]
assert "Timesheet" in h3_text, "timesheet page not found" and browser.save_screenshot(
    "timesheet_not_found.png"
)


# click on the time entries
time_sheet_form = browser.find_element(By.TAG_NAME, "form")

# this will be for link in links, but it ammounts to finding the "add time entry" link


#printts all the text of all the links
days_to_fill=browser.find_elements(By.CLASS_NAME,"TimesheetSlat TimesheetSlat--clock TimesheetSlat--expandable")
print(days_to_fill)
# list_of_links=[link.get_attribute("innerHTML") for link in links]
days_objs = browser.find_elements(By.CLASS_NAME, "TimesheetSlat__dayOfWeek")
week = [day.text for day in days_objs]
# mane timesheet page here
WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.TAG_NAME, "a")))

for link in days_to_fill:

    link= WebDriverWait(browser, 10).until(EC.element_to_be_clickable(link))

    link.click()

    index_no = links.index(link)

    # if week day link is sunday or saturday, skip and don't fill in the hours
    if (week[index_no] == "Sun") or (week[index_no] == "Sat"):
        continue

    # if its a bank holiday or annual leave don't fill it in

    if browser.find_element(
        locate_with(
            By.XPATH,
            "//div[@class='TimesheetSlat__extraInfoItem TimesheetSlat__extraInfoItem--clockPush']",
        )
    ).below(link):
        continue

    # check how many hours you have worked for that particular day

    day_total = browser.find_element(By.CLASS_NAME, "AddEditEntry__dayTotal")
    hours_worked = day_total.text

    # locate input box and drop down menu, as well as the buttons
    input_box = browser.find_element(By.ID, "hoursWorked")
    drop_down = browser.find_element(
        By.XPATH, "//div[text()='--Select Project/Task--']"
    )
    save_button = browser.find_element(By.XPATH, "//span[text()='Save']")

    # fill in time sheet if hours worked appear 0:
    if hours_worked == "Day Total: 0h 00m":
        input_box.send_keys("7.5")

    # make sure to always indicate the automation and ai department and save the options
    drop_down.click()
    department = browser.find_element(By.CSS_SELECTOR, ".fab-MenuOption__row").click()
    save_button.click()

    if index_no == (len(days_to_fill) - 1):
        print("time sheet filled")

browser.save_screenshot("timesheet.png")
browser.quit()
# else:
#    print("no need to fill in the time sheet today")


# hours=browser.find_element(By.XPATH, "//div[text()='Day Total: 7h 30m']")

# print(bool(hours))


# for day in week:
# click the day you need to fill in:
# browser.find_element(By.XPATH, f"//span[text()='{day}']")
#   click("Add Time Entry")
#  if Text("Day Total: 7h 30m").exists() or Text("Day Total: 8h").exists():
#     click("Cancel")  # if there are alreaddy hrs logged in skip
# /html/body/div[3]/section/div[2]/div[2]/div/div[3]/div[1]/form/div[4]/div[2]/div/div[1]/a
# else:  # log the hours and click save
#  write("7.5")
#   click("--Select Project/Task--")
# click("Liberty Global Automation & AI")
# click("Save")
# confirm that we are back to the timesheet page
# assert Text("Timesheet").exists()


# to do:
#  configure the wait for clicable element in python
# do the logic for not filling in the sheet on weekends
# double check that the calendar logic works
# configure the github action to fill the worksheet
# double check the screenshot logic
