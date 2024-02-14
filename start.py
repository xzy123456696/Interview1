from selenium import webdriver
from selenium.webdriver.chrome.service import Service  # Import the Service class
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time

# Check if date and currency code arguments are provided
if len(sys.argv) != 3:
    print("Usage: python3 yourcode.py YYYYMMDD CURRENCY_CODE")
    sys.exit(1)

# Extract arguments from the command line
input_date = sys.argv[1]  # Format: YYYYMMDD
currency_code = sys.argv[2]  # Example: USD

options = webdriver.ChromeOptions()
chromDriver_path = '/Users/ziyixu/Desktop/国内实习/DreamSchool/第一轮面试/chromedriver'
service = Service(chromDriver_path)
driver = webdriver.Chrome(service= service, options=options)
chineseName = None
try:
    driver.get('https://www.11meigui.com/tools/currency')
    standSignal = driver.find_element(By.XPATH,'//tbody/table/tbody/tr')
    for item in standSignal[1:]:
        if item.find_element(By.XPATH,'//td[4]').text == currency_code:
            chineseName = item.find_element(By.XPATH,'//td[1]').text
            break
except Exception as e:
    print(f"error: {e}")
finally:
    driver.quit()

options = webdriver.ChromeOptions()
chromDriver_path = '/Users/ziyixu/Desktop/国内实习/DreamSchool/第一轮面试/chromedriver'
service = Service(chromDriver_path)
driver = webdriver.Chrome(service= service, options=options)
try:
    driver.get('https://www.boc.cn/sourcedb/whpj/')
     # wait load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pjname"))
    )
    # Select the currency from the dropdown
    currency_select = Select(driver.find_element(By.ID, "pjname"))
    currency_select.select_by_value(chineseName)
    if currency_select == None:
        print("Can't Find Correspond Chinese Name")
    else: 
        # enter the data
        date_input = driver.find_element(By.NAME, 'erectDate')
        currency_input = driver.find_element(By.ID, "pjname")
        date_input.clear()
        date_input.send_keys(input_date)
        currency_input.send_keys(currency_select)
        # Submit the form
        search_button = driver.find_element(By.XPATH, '//input[@type="submit"]')
        search_button.click()
        # wait load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "publish"))
        )
        # Assuming the first row of results contains the data we want
        # and that "cash selling price" is the 7th column in the table
        cash_selling_price = driver.find_element(
            By.XPATH, '//table/tbody/tr[2]/td[4]'
        ).text

    # Print and write the result to a text file
    print(cash_selling_price)
    with open('result.txt', 'w') as file:
        file.write(cash_selling_price)

except Exception as e:
    print(f"error: {e}")
finally:
    driver.quit()