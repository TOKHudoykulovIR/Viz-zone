from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from datetime import datetime, timedelta

import time
import re

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://__base_url__/")
time.sleep(1)

# LOGIN 
login = driver.find_element(by=By.CSS_SELECTOR, value="input[id='login']")
password = driver.find_element(by=By.CSS_SELECTOR, value="input[id='password']")

login.clear()
login.send_keys('__login__')

time.sleep(0.5)

password.clear()
password.send_keys('__password__')

time.sleep(1)
yesterday = (datetime.today() - timedelta(days=2)).strftime('%d.%m.%Y')
driver.get(f"https://__base_url__/#/__path__/from={yesterday}&to={yesterday}&status=1&limit=25")
time.sleep(1)

def get_total_sum():  # GET TOTAL SUM
    total_sum_text = driver.find_element(By.CSS_SELECTOR, value="div.table_info div.row > div:nth-child(3) p").text
    total_sum_text_number = re.findall(r'\d+', total_sum_text)
    total_sum = ''.join(total_sum_text_number)
    return total_sum

concated = ''

#  ___  1 GET TOTAL PAYMENT TRANSACTIONS WITHOUT DIRECT P2P  ___
tot_payment_no_direct_p2p = get_total_sum()
print(f"Total payment  :  {tot_payment_no_direct_p2p}")

#  ___  ITERATE CATEGORIES  ___
for category_value in ['14', '3', '125', '25']:  # mob, internet, utilities, gov.services:
    #  ___  SELECT CATEGORY  ___
    Select(driver.find_element(By.CSS_SELECTOR, value="select[name='group']")).select_by_value(category_value)

    driver.find_element(By.CSS_SELECTOR, value="form button.submit").click()  # CLICK TO SEARCH
    time.sleep(3)
    
    #  ___  2 GET CATEGORIES TRANSACTIONS SUM  ___
    category_sum = get_total_sum()
    print(f"{category_value}  :  {category_sum}")
    concated += f" {category_sum}"

#  ___  3 Wallet > Wallet  ___
driver.get(f"https://__base_url__/#/__path__/from={yesterday}&to={yesterday}&merchant=id&status=1&manufacturer=3&limit=25")
time.sleep(2)
o_to_o_sum = get_total_sum()
print(f"Wallet > Wallet  :  {o_to_o_sum}")

concated = f'{o_to_o_sum} {tot_payment_no_direct_p2p}{concated}'
print(concated)

yesterday = (datetime.today() - timedelta(days=2)).strftime('%d.%m.%Y')

driver.get(f"https://__base_url__/__path__/?from={yesterday}&to={yesterday}&m_id=-12&status=1")
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, value="form button.submit").click()  # CLICK TO SEARCH
time.sleep(1)
tds = driver.find_elements(By.CSS_SELECTOR, value='table td:nth-child(2)')

for step, td in enumerate(tds):
    if 'UZCARD > UZCARD' in td.text:
        merchant = 'UZCARD > UZCARD'
        u_to_u = driver.find_elements(By.CSS_SELECTOR, value='table td:nth-child(3)')[step].text[:-2]
        u_to_u_digits = re.findall(r'\d+', u_to_u)
        u_to_u_formatted = ''.join(u_to_u_digits)
        print(f"{merchant}  :  {u_to_u_formatted}")
    elif 'HUMO > HUMO' in td.text:
        merchant = 'HUMO > HUMO'
        h_to_h = driver.find_elements(By.CSS_SELECTOR, value='table td:nth-child(3)')[step].text[:-2]
        h_to_h_digits = re.findall(r'\d+', h_to_h)
        h_to_h_formatted = ''.join(h_to_h_digits)
        print(f"{merchant}  :  {h_to_h_formatted}")
        
concated = f'{h_to_h_formatted} {u_to_u_formatted} {concated}'
print(concated)

driver.get(f"https://__base_url__/__path__/?from={yesterday}&to={yesterday}&m_id=&status=1")
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, value="form button.submit").click()  # CLICK TO SEARCH
time.sleep(2)

def get_td_value(merchant):
    global breaker
    merchant_to_merchant = driver.find_elements(By.CSS_SELECTOR, value='table td:nth-child(3)')[step].text[:-2]
    merchant_to_merchant_digits = re.findall(r'\d+', merchant_to_merchant)
    merchant_to_merchant_formatted = ''.join(merchant_to_merchant_digits)
    print(f"breaker({breaker}),  {merchant}  :  {merchant_to_merchant_formatted}") 
    breaker -= 1
    return merchant_to_merchant_formatted

breaker = 4
tds = driver.find_elements(By.CSS_SELECTOR, value='table td:nth-child(2)')

for step, td in enumerate(tds):
    if 'UZCARD > HUMO' in td.text:
        merchant = 'UZCARD > HUMO'
        u_to_h_formatted = get_td_value(merchant)
    elif 'HUMO > UZCARD' in td.text:
        merchant = 'HUMO > UZCARD'
        h_to_u_formatted = get_td_value(merchant)
    elif 'Wallet > HUMO' in td.text:
        merchant = 'Wallet > HUMO'
        o_to_h_formatted = get_td_value(merchant)
    elif 'Wallet > UZCARD' in td.text:
        merchant = 'Wallet > UZCARD'
        o_to_u_formatted = get_td_value(merchant)

    if not breaker:
        break
        
concated = f'{u_to_h_formatted} {h_to_u_formatted} {o_to_u_formatted} {o_to_h_formatted} ' + concated
print(concated)
