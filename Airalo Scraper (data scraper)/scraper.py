"""
Scraper to get data about tariffs from Airalo service to further analytics
"""

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from datetime import datetime, timedelta

import time
import re

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://www.airalo.com/")
time.sleep(1)

countries = driver.find_elements(By.CSS_SELECTOR, value='.store-item.aloo a')
print(len(countries), '\n')

for step, country in enumerate(countries): 
    if step < 200:
        continue
        
    print(country.get_attribute('href'))
    driver.execute_script("window.open('%s', '_blank')" % country.get_attribute('href'))
    time.sleep(1)

    # Switch to new tab
    driver.switch_to.window(driver.window_handles[-1])
    
    country_name = driver.find_element(By.CSS_SELECTOR, value='h2#store-title').text
    # print(country_name)

    values = driver.find_elements(By.CSS_SELECTOR, value='.package-list-wrapper ul li p.value')
    for value in values:
        if country_name not in value.text:
            print(value.text)
            
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    if step == 204:
        break
    print("\n")
