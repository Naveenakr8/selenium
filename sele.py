import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from  selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import re
# Code for restricting the browser for not closing automatically
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("start-maximized")
# handling notifications
chrome_options.add_argument("--use-fake-ui-for-media-stream")

# chrome driver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# Verification of Email and Password
email_pattern = r'^[\w.-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,}$'
password_pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@])[A-Za-z\d@]{8,}$'
valid_credentials = True
while valid_credentials:
  USER1_EMAIL = input("Enter User 1 email address: ")
  USER1_PASSWORD = input("Enter User 1 password: ")
  if re.match(email_pattern, USER1_EMAIL):
    if re.match(password_pattern, USER1_PASSWORD):
      valid_credentials = False
    else:
      print("Invalid Password. Please try again.")
    valid_credentials = False
  else:
    print("Invalid email address. Please try again.")

# Initializing the web driver
service_obj = Service("C:/Users/SMOHANNA/Downloads/chromedriver_win32/chromedriver.exe")
driver = webdriver.Chrome(options=chrome_options, service=service_obj)
driver.minimize_window()

# Function to log in to Microsoft Teams
def login(email, password):
    try:
        driver.implicitly_wait(4)
        driver.get("https://teams.microsoft.com")
        driver.maximize_window()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "loginfmt")))
        driver.find_element(By.NAME, "loginfmt").send_keys(email)
        driver.find_element(By.XPATH, "//input[@type='submit']").click()
        time.sleep(5)
        driver.find_element(By.NAME, "passwd").send_keys(password)
        time.sleep(5)
        driver.find_element(By.XPATH, "//input[@value='Sign in']").click()
        time.sleep(5)
        # Verifying the user1 is logged in
        try:
            kmsi_description = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "KmsiDescription")))
        except:
            error_message_element = driver.find_element(By.ID, "passwordError")
            error_message = error_message_element.text if error_message_element.is_displayed() else "Unknown error occurred."
            print(f"User 1 Login failed. Error message: {error_message}")
        driver.find_element(By.ID, "idBtn_Back").click()
        time.sleep(10)
        driver.get("https://www.google.com")
        driver.back()
        driver.find_element(By.LINK_TEXT, "Use the web app instead").click()
        driver.get("https://www.google.com")
        driver.back()
        # Verifying the user 1 is logged in
        user_profile = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "personDropdown")))
        action = ActionChains(driver)
        action.move_to_element(user_profile).click().perform()
        time.sleep(5)
        user_profile_id = driver.find_element(By.XPATH, "//span[text() = 'shrirajofc01@gmail.com']").text
        if user_profile_id == USER1_EMAIL:
            print("User 1 logged in successfully")
            driver.find_element(By.ID, "personDropdown").click()
        else:
            print("User 1 login was failed")

        # Function to search and call a user
        time.sleep(5)
        dropdown = driver.find_element(By.ID, "searchInputField")
        dropdown.send_keys("Raj N")
        time.sleep(5)
        dropdown.send_keys(Keys.DOWN)
        dropdown.send_keys(Keys.ENTER)
        driver.find_element(By.XPATH, "//button[@title='Audio call']").click()
        # Function for declining the call
        time.sleep(5)
        driver.find_element(By.XPATH, "//div[text()='Dismiss']").click()
        iframe = driver.find_element(By.XPATH, "//div[@id='ExperienceContainerManagerMountElement']/div/iframe")
        driver.switch_to.frame(iframe)
        while True:
            WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//span[@data-tid='call-duration']")))
            times = driver.find_element(By.XPATH, "//span[@data-tid='call-duration']").text
            # print(times)
            if times == "01:00":
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//button[@id='hangup-button']")))
                driver.find_element(By.XPATH, "//button[@id='hangup-button']").click()
                break
        # Function for sending the message
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[7]/div[1]/div[1]/div[3]/div[1]/div[4]/div[1]/div[3]/div[1]/p[1]")))
        driver.find_element(By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[7]/div[1]/div[1]/div[3]/div[1]/div[4]/div[1]/div[3]/div[1]/p[1]").send_keys("Dropped the call")
        actions = webdriver.ActionChains(driver)
        time.sleep(5)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        driver.switch_to.default_content()
        # Logout from user 1
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "personDropdown")))
        driver.find_element(By.ID, "personDropdown").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "logout-button")))
        driver.find_element(By.ID, "logout-button").click()
        if driver.find_element(By.XPATH, "//button[@data-tid='tidConfirmButton']"):
            driver.find_element(By.XPATH, "//button[@data-tid='tidConfirmButton']").click()
            print("User 1 logged out successfully")
        else:
            print("User 1 logged out successfully")
            #login(USER1_EMAIL, USER1_PASSWORD)
    except NoSuchElementException:
      print("Element not found. Check if the login page structure has changed.")
    except TimeoutException:
      print("Element not found")
    except Exception as e:
        print("Exception occurred:", e)


