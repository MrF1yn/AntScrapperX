import random
import time
import redis
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

# Configure WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")
options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
driver = webdriver.Chrome(options=options)

# Timeout settings
timeout = 10

# CSV file setup
output_file = "ajio_results.csv"
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Phone Number", "Status"])  # Write the header row

    try:
        # Open the Ajio website
        driver.get("https://www.ajio.com")
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        while True:
            # Pull a phone number from the Redis list (blocking call)
            result = redis_client.brpop("ajio", timeout=30)  # Adjust the timeout as needed
            if not result:
                print("No more numbers to process. Exiting.")
                break

            phone_number = result[1]  # Decode the number from bytes
            print(f"Processing phone number: {phone_number}")

            status = "Error"
            try:
                # Click the Signup button
                signup_button = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, "//span[@id='loginAjio']"))
                )
                signup_button.click()

                # Enter the phone number
                phone_input = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='number' and @name='username']"))
                )
                phone_input.clear()
                phone_input.send_keys(phone_number)

                # Click the Continue button
                continue_button = driver.find_element(By.XPATH, "//input[@value='Continue']")
                continue_button.click()

                # Wait for the popup and check the result
                popup = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//h2[text()='Please set up your account' or text()='Please enter OTP sent to']")
                    )
                )
                if "account" in popup.text:
                    status = "Absent"
                elif "OTP" in popup.text:
                    status = "Present"

                print(f"Number {phone_number}: {status}")
                redis_client.lpush("ajio_results", f"{phone_number},{status}")

            except Exception as e:
                print(f"Error processing number {phone_number}: {str(e)}")

            finally:
                # Close the popup
                try:
                    close_button = driver.find_element(By.XPATH, "//div[@id='closeBtn']")
                    close_button.click()
                    # time.sleep(random.uniform(0.5, 1.5))
                except Exception as e:
                    print(f"Error closing popup for number {phone_number}: {e}")

                # Log the result in the CSV file
                writer.writerow([phone_number, status])
                  # Ensure data is written to the file immediately

                # Delay before processing the next number
                time.sleep(0.5)

    finally:
        # Close the browser
        driver.quit()
        file.flush()
