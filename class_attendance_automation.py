from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import pytz  # Ensure pytz is installed with 'pip install pytz'

def join_class():
    driver = None
    username = ''
    password = ''
    morning_class_token = 'd261fa47-06bf-3b66-90fa-b966ca86c7ce'
    evening_class_token = '63bc6c4d-920f-36f8-bdc0-456a08f813c9'

    try:
        service = Service(r'C:\Selenium\chromedriver-win64\chromedriver.exe')
        driver = webdriver.Chrome(service=service)

        driver.get('https://myclass.lpu.in/')
        driver.find_element(By.NAME, 'i').send_keys(username)
        driver.find_element(By.NAME, 'p').send_keys(password)
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[aria-label="View Classes and Meetings"]'))
        ).click()

        india_timezone = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(india_timezone)
        token = morning_class_token if current_time.hour < 12 else evening_class_token

        class_link_xpath = f"//a[@title='CSES010-Lecture by :  65634:Laxmikant Deshpande ( 9W097CSES01024252 ) ' and contains(@href, '{token}')]"
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, class_link_xpath))
        ).click()

        join_link_xpath = f"a[href='/secure/tla/jnr.jsp?m={token}']"
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, join_link_xpath))
        ).click()

        print("Successfully joined the class.")
        
        # Stay in the class for 2 hours
        time.sleep(7200)  # 7200 seconds = 2 hours

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        if driver:
            driver.quit()

# Execute the function
join_class()
