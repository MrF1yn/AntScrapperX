import random

import redis
import json
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)
scrapper_id = random.randint(100000, 999999)
start_time = int(time.time() * 1000)
# Redis Configuration
REDIS_CONFIG = {
    'host': 'redis-19800.crce179.ap-south-1-1.ec2.redns.redis-cloud.com',
    'port': 19800,
    'username': 'default',
    'password': 'JMPog04EGI2MVcbO3HDPC9clDNyztfBX',
    'decode_responses': True
}

# Queue names
REDIS_INPUT_QUEUE = 'microsoft_email'
REDIS_OUTPUT_QUEUE = 'microsoft_email_results'


def setup_chrome_driver():
    """Set up Chrome driver with appropriate options."""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-infobars')
    return webdriver.Chrome(options=options)


def extract_relevant_text(page_content: str) -> str:
    """Extract relevant text from page content using regex patterns."""
    patterns = [
        r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}) is already a Microsoft account',
        r'Enter the email address in the format someone@example\.com',
        r'Create a password',
    ]

    for pattern in patterns:
        match = re.search(pattern, page_content)
        if match:
            return match.group(0)
    return 'No relevant information found in the response.'


def process_email(driver, email: str) -> str:
    """Process a single email and return the result."""
    start_time = time.time()

    try:
        # Navigate to signup page
        driver.get('https://signup.live.com/signup')

        # Wait for and fill email input
        email_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "usernameInput"))
        )
        email_input.clear()
        email_input.send_keys(email)

        # Wait for and click next button
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "nextButton"))
        )
        next_button.click()

        # Wait for response
        time.sleep(2)

        # Get and process page content
        page_content = driver.page_source
        relevant_text = extract_relevant_text(page_content)

        end_time = time.time()
        return f"{scrapper_id},{email},{relevant_text},{int(time.time() * 1000)}"
        # return {
        #     'uid': email_data['uid'],
        #     'email': email_data['email'],
        #     'response': relevant_text,
        #     'start_time': datetime.fromtimestamp(start_time).isoformat(),
        #     'end_time': datetime.fromtimestamp(end_time).isoformat(),
        #     'duration': round((end_time - start_time) * 1000, 2)  # Duration in milliseconds
        # }

    except Exception as e:
        end_time = time.time()
        error_msg = str(e)
        logger.error(f"Error processing email {email}: {error_msg}")
        return f"{scrapper_id},{email},ERROR,{int(time.time() * 1000)}"
        # return {
        #     'uid': email_data['uid'],
        #     'email': email_data['email'],
        #     'response': f'Error occurred: {error_msg}',
        #     'start_time': datetime.fromtimestamp(start_time).isoformat(),
        #     'end_time': datetime.fromtimestamp(end_time).isoformat(),
        #     'duration': round((end_time - start_time) * 1000, 2)
        # }


def main():
    """Main execution function."""
    script_start_time = time.time()
    logger.info("Starting email processing script")

    # Connect to Redis
    try:
        redis_client = redis.Redis(**REDIS_CONFIG)
        logger.info("Connected to Redis successfully")
    except Exception as e:
        logger.error(f"Failed to connect to Redis: {e}")
        return

    driver = None
    try:
        # Get total number of emails
        total_emails = redis_client.llen(REDIS_INPUT_QUEUE)
        if total_emails == 0:
            logger.info("No emails found in the Redis input queue")
            return

        logger.info(f"Found {total_emails} emails to process")

        # Initialize Selenium WebDriver
        driver = setup_chrome_driver()

        processed_count = 0
        while processed_count < total_emails:
            # Get email from the end of the queue (right side)
            email = redis_client.brpop(REDIS_INPUT_QUEUE)
            if not email:
                print("No more numbers to process. Exiting.")
                # print(f"Total execution time: {time.time() - total_start_time:.2f} seconds")
                break
            email = email[1]

            # Process the email
            logger.info(f"Processing email: {email}")
            result = process_email(driver, email)

            # Store result
            redis_client.lpush(REDIS_OUTPUT_QUEUE, result)
            processed_count += 1
            logger.info(f"Processed {processed_count}/{total_emails} emails")

    except Exception as e:
        logger.error(f"Script error: {e}")

    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                logger.error(f"Error closing driver: {e}")

        script_end_time = time.time()
        total_duration = round(script_end_time - script_start_time, 2)
        logger.info(f"Script completed. Total duration: {total_duration} seconds")
        redis_client.close()


if __name__ == "__main__":
    main()