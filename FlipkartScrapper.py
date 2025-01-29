import os
import random
import redis
import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
scrapper_id = random.randint(100000, 999999)
start_time = int(time.time() * 1000)

def set_viewport_size(driver, width, height):
    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)


redis_client = redis.Redis(
    host='redis-19800.crce179.ap-south-1-1.ec2.redns.redis-cloud.com',
    port=19800,
    decode_responses=True,
    username="default",
    password="JMPog04EGI2MVcbO3HDPC9clDNyztfBX",
)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Brave/91.1.25.73",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
]

# Configure the WebDriver (Ensure to have the correct driver installed and added to PATH)
options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")
options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
# options.add_argument(f"--user-data-dir=/tmp/chrome-data")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument('--no-sandbox')
options.add_argument("--window-size=1920,1080")
  # Unique user data directory

# Replace `webdriver.Chrome()` with the appropriate WebDriver instance if you're not using Chrome
driver = webdriver.Chrome(options=options)

driver.get("https://www.flipkart.com/account/login?signup=true")

try:
    body_present = EC.presence_of_element_located((By.TAG_NAME, "body"))
    WebDriverWait(driver, 10).until(body_present)
except Exception as e:
    print(f"Error: {e}")
set_viewport_size(driver, 820, 756)

# Prepare to write to CSV
with open('flipkart_results.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Phone Number", "Status"])  # CSV Header

    # Fetch phone numbers from Redis list using BRPOP
    while True:
        # Block and wait for a phone number from the Redis list 'flipkart_phone_list'
        phone_number = redis_client.brpop('flipkart', timeout=30)  # timeout=0 means it blocks indefinitely
        if not phone_number:
            print("No more numbers to process. Exiting.")
            end_time = int(time.time() * 1000)
            print(f"Runtime: {end_time - start_time}ms")
            break
        if phone_number:  # phone_number is a tuple, e.g., (key, value)
            phone_number = phone_number[1]  # Extracting the phone number and converting bytes to string

            present = 0
            try:
                # Wait for the phone number input field to appear
                phone_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "(//input[@type='text'])[2]"))
                )
                phone_input.click()
                phone_input.clear()
                phone_input.send_keys(phone_number)

                # Click on continue button
                continue_button = driver.find_element(By.XPATH, "(//button[@type='submit'])[2]")
                continue_button.click()

                # Wait for popup to appear and process the result
                popup = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//button[text()='Request OTP' or span[text()='Signup']] | //span[text()='Please enter a valid Mobile number']"))
                )

                if "Signup" in popup.text:
                    print(f"Number {phone_number}: Absent")
                    redis_client.lpush("flipkart_results", f"{scrapper_id},{phone_number},Absent,{int(time.time() * 1000)}")
                    present = 0
                elif "OTP" in popup.text:
                    print(f"Number {phone_number}: Present")
                    redis_client.lpush("flipkart_results", f"{scrapper_id},{phone_number},Present,{int(time.time() * 1000)}")
                    present = 1
                elif "valid" in popup.text:
                    print(f"Number {phone_number}: Invalid")
                    redis_client.lpush("flipkart_results", f"{scrapper_id},{phone_number},Invalid,{int(time.time() * 1000)}")
                    present = 2

                # Save result to CSV
                writer.writerow(
                    [phone_number, "Present" if present == 1 else ("Absent" if present == 0 else "Invalid")])
                # file.flush()  # Flush the content to disk immediately

            except Exception as e:
                print(f"Error processing number {phone_number}")

                writer.writerow([phone_number, "Error"])
                # file.flush()  # Flush the content to disk immediately

            finally:
                # time.sleep(2)  # Wait briefly for the page to reload
                try:
                    close_button = None
                    if present == 1:
                        close_button = driver.find_element(By.XPATH,
                                                           "//a[contains(text(), 'Create an account')]/parent::div")
                        close_button.click()
                    elif present == 0:
                        close_button = driver.find_element(By.XPATH, "//a[@href='#' and span[text()='Change?']]")
                        close_button.click()
                except Exception as e:
                    print(f"Error closing popup for number {phone_number}")
                time.sleep(2)  # Wait briefly for the page to reload
    file.flush()

# Close the browser
    driver.quit()
