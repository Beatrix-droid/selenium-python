from calendar import monthrange
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from webdriver_manager.firefox import GeckoDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import os
import logging


# import logging
logging.basicConfig(level=logging.INFO,  format='%(asctime)s :: %(levelname)s :: %(message)s')

# initialise browser

# check if it is friday or the end of the month:
logging.info("starting the automation job")
current_day = date.today()

logging.info(f"today is {current_day.strftime('%A')} and the day of the month is {current_day.day}")
# check that its friday or the last day of the month
# if (current_day.strftime("%A")== "Friday") or (current_day.day==monthrange(current_day.year, current_day.month)[1]) :
logging.info("filling in the time sheet")


# configure the browser driver
options = FirefoxOptions()
options.add_argument("start-maximized")
options.binary = FirefoxBinary("/usr/bin/firefox")

firefox_service = FirefoxService(GeckoDriverManager().install())

#check where to get the env variables, LOCAL is for development and debugging, else default to productions setup:
hostname= os.getenv("WHEREAMI")
if hostname=="LOCAL":
    logging.info("environment is local, using local env variables")
    from config import credentials
    USER_NAME=credentials["username"]
    USER_PASSWORD=credentials["password"]
else:
    USER_NAME = os.environ.get("USERNAME") #for production
    USER_PASSWORD = os.environ.get("PASSWORD")
    options.add_argument("--headless")
    logging.info("environment is prod, using local gh secrets and instantiating a headless browser")



# initialise an instance of the browser
browser = webdriver.Firefox(service=firefox_service, options=options)
browser.implicitly_wait(10)  # change the default wait to 10

# create action chain object
action = ActionChains(browser)

# navigate to the login page
browser.get("https://softwareinstitute.bamboohr.com/login.php")

logging.info("navigating to the login form")
sleep(2)
# check if login page has loaded correctly
spans = browser.find_elements(By.TAG_NAME, "span")
text_spans = [span.text for span in spans]

page_has_loaded = bool("Log in with SAML" in text_spans)

if not page_has_loaded:
    browser.save_full_page_screenshot("faulty_login.png")
    logging.error("login page not loaded correctly, exiting script")
    browser.quit()
    quit()

logging.info("navigated to login form")
# click 'login with email and password':
normal_login_button = browser.find_element(
    By.XPATH, "//button[contains(text(),'Log in with Email and Password')]"
).click()

# identify login form and check that it has loaded correctly:
email = browser.find_element(By.CSS_SELECTOR, "#lemail")
password = browser.find_element(By.CSS_SELECTOR, "#password")
submit_button = browser.find_element(By.XPATH, "//span[text()='Log In']")


# type into form
email.send_keys(USER_NAME)
password.send_keys(USER_PASSWORD)

# Submit form
submit_button.click()


sleep(2)
# content = driver.find_element(By.CSS_SELECTOR, 'p.content')  to locate by class
try:
    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
    my_title= WebDriverWait(browser, 10 ,ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.XPATH, "//span[text()='Graduate Technical Consultant']")))
except:
    browser.save_full_page_screenshot("home_page_not_found.png")
    logging.error("homepage not loaded correctly, exiting script")
    browser.quit()
    quit()

logging.info("logged in")

# locate my "my timesheet" button and click on it
my_timesheet = browser.find_element(By.LINK_TEXT, "My Timesheet")
my_timesheet.click()


# check that we have navigated to the timesheet page:
sleep(2)
h3_tags = browser.find_elements(By.TAG_NAME, "h3")

# quit if session is not valid any more
if browser is None:
    browser.quit()
    logging.error("session got disconnected, terminating script")
    quit()


h3_text = [tag.text for tag in h3_tags]
if "Timesheet" not in h3_text:
    logging.error("timehseet not loaded correctly")
    browser.save_screenshot("timesheet_not_found.png")
    browser.quit()
    quit()

logging.info("navigated to timesheet")

# click on the time entries
time_sheet_form = browser.find_element(By.TAG_NAME, "form")

days_to_fill = time_sheet_form.find_elements(By.TAG_NAME, "a")

logging.info(f"found {str(len(days_to_fill))} to click on. Starting to fill in the timesheet")


# main timesheet page here

for link in days_to_fill:

    sleep(2)
    logging.info(f"clicking on link no {str(days_to_fill.index(link))}")
    browser.execute_script("arguments[0].scrollIntoView();", link)
    action.move_to_element(link)
    action.perform()

    browser.execute_script("arguments[0].click();", link)
    sleep(2)

    # need to implement logic for if its a bank holiday or annual leave don't fill it in

    # check what day of the week it is
    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
    h4_tags= WebDriverWait(browser, 10 ,ignored_exceptions=ignored_exceptions)\
                        .until(EC.presence_of_all_elements_located((By.TAG_NAME, "h4")))
    h4_text=[h4_tag.text for h4_tag in h4_tags]
    day=h4_text[-1].split()[0]


    # if week day is Sunday or Saturday, skip and don't fill in the hours
    if ("Sunday" in day) or ("Saturday" in day):
        logging.info(f"day is a {day} skipping this day")
        cancel_button = browser.find_element(By.XPATH, "//span[text()='Cancel']")
        browser.execute_script("arguments[0].click();", cancel_button)
        logging.info("moved onto the next day")
        continue

    # check how many hours you have worked for that particular day
    sleep(2)
    day_total = browser.find_element(By.CLASS_NAME, "AddEditEntry__dayTotal")
    hours_worked = day_total.text

    #if hours are already filled for that day skip filling that day in
    if hours_worked == "Day Total: 7h 30m":
        logging.info(f"hours worked already present are {hours_worked}, skipping this day")
        cancel_button = browser.find_element(By.XPATH, "//span[text()='Cancel']")
        browser.execute_script("arguments[0].click();", cancel_button)
        logging.info("moved onto the next day")
        continue


    # else locate input box and drop down menu, as well as the save buttons
    input_box = browser.find_element(By.ID, "hoursWorked")
    drop_down = browser.find_element(
        By.XPATH, "//div[text()='--Select Project/Task--']"
    )
    save_button = browser.find_element(By.XPATH, "//span[text()='Save']")

    # fill in time sheet if hours worked appear 0:
    if hours_worked == "Day Total: 0h 00m":
        logging.info(f"entering in hours for {day}")
        input_box.send_keys("7.5")

        # make sure to always indicate the automation and ai department and save the options
        drop_down.click()
        department = browser.find_element(By.CSS_SELECTOR, ".fab-MenuOption__row").click()
        browser.execute_script("arguments[0].click();", save_button)
        logging.info("hours successfully entered, moved onto the next day")


logging.info("time sheet filled")
sleep(5)

browser.save_full_page_screenshot("timehseet.png")
logging.info("Screenshot with timesheet filled saved! Now logging out")
# log out and quit browser

browser.get("https://softwareinstitute.bamboohr.com/logged_out.php")
sleep(1)
logging.info("Successfully logged out")
browser.quit()
sleep(1)
logging.info("Closed browser")
# else:
#    logging.info("no need to fill in the time sheet today")
