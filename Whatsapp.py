import base64
import json
import os
import random
import time
from io import BytesIO

import redis
import csv

from PIL import Image
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from util.qr_to_ascii import convert_qr_to_ascii

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
prefs = {
    "profile.default_content_settings.geolocation": 1,
    "profile.content_settings.exceptions.geolocation": {
        "https://www.example.com": {"setting": 1, "latitude": 28.6139, "longitude": 77.2090}
    }
}

options.add_experimental_option("prefs", prefs)
options.add_argument("--log-level=3")
options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
driver = webdriver.Chrome(options=options)

# Timeout settings
timeout = 30

# CSV file setup
output_file = "whatsapp_results.csv"
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Phone Number", "Status"])  # Write the header row

    try:
        # Open the whatsapp website
        driver.get("https://web.whatsapp.com")
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        login = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//div[text() = 'Log in with phone number']"))
        )
        login.click()

        # country_dropdown = WebDriverWait(driver, timeout).until(
        #     EC.presence_of_element_located(By.XPATH, "//button[.//span[contains(@data-icon, 'chevron')]]")
        # )
        # country_dropdown.click()



        phone_number_field = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Type your phone number.']"))
        )
        phone_number_field.click()
        phone_number = "8145874011"
        phone_number_field.send_keys(phone_number)

        next_button = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[.//div[contains(text(), 'Next')]]"))
        )

        next_button.click()



        WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((By.XPATH,
                                                                             "//span[text() and string-length(normalize-space(text())) = 1 and translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', '') = '']")))

        # Find all the spans matching the XPath
        spans = driver.find_elements(By.XPATH,
                                     "//span[text() and string-length(normalize-space(text())) = 1 and translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', '') = '']")

        # Print the text of each span
        for span in spans:
            print(span.text, end='')

        # canvas = WebDriverWait(driver, timeout).until(
        #     EC.presence_of_element_located((By.XPATH, "//canvas[@aria-label[contains(., 'Scan')]]"))
        # )
        # print("Scan the QR code to login to WhatsApp Web.")
        # canvas_data = driver.execute_script("""
        #     var canvas = arguments[0];
        #     return canvas.toDataURL('image/png').substring(22);  // Remove 'data:image/png;base64,' prefix
        # """, canvas)
        # image_data = base64.b64decode(canvas_data)
        # image = Image.open(BytesIO(image_data))
        # convert_qr_to_ascii(image, False)
        new_chat = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//button[@aria-label='New chat']"))
        )
        new_chat.click()
        while True:
            # Pull a phone number from the Redis list (blocking call)
            result = redis_client.brpop("whatsapp", timeout=30)  # Adjust the timeout as needed
            if not result:
                print("No more numbers to process. Exiting.")
                break

            phone_number = result[1]  # Decode the number from bytes
            print(f"Processing phone number: {phone_number}")
            status = "Error"
            try:

                # Enter the phone number
                focused_element = driver.switch_to.active_element
                focused_element.send_keys(Keys.CONTROL + "a")
                focused_element.send_keys(Keys.BACKSPACE)
                focused_element.send_keys(phone_number)

                # Click the Continue button

                # Wait for the popup and check the result
                popup = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//span[contains(text(), 'No results found for')] | //div[contains(text(), 'Not in your contacts')]")
                    )
                )
                if "No results" in popup.text:
                    status = "Absent"
                else:
                    status = "Present"

                print(f"Number {phone_number}: {status}")
                redis_client.lpush("whatsapp_results", f"{phone_number},{status}")

            except Exception as e:
                print(f"Error processing number {phone_number}: {str(e)}")

            finally:
                # Close the popup

                # Log the result in the CSV file
                writer.writerow([phone_number, status])
                  # Ensure data is written to the file immediately

                # Delay before processing the next number
                time.sleep(0.5)

    finally:
        # Close the browser
        driver.quit()
        file.flush()
