
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import pandas as pd
# import time

# def automate_login():
#     # Read the Excel file
#     try:
#         df = pd.read_excel('newest_file.xlsx')
#         phone_numbers = df.iloc[:, 1]  # Get the second column
#     except Exception as e:
#         print(f"Error reading Excel file: {e}")
#         return

#     base_url = "https://login.live.com/oauth20_authorize.srf?client_id=10fa57ef-4895-4ab2-872c-8c3613d4f7fb&scope=openid+profile+offline_access&redirect_uri=https%3a%2f%2fwww.microsoft.com%2fcascadeauth%2faccount%2fsignin-oidc&response_type=code&state=CfDJ8P_pstto1o1NgBRsh8q_VvgvqWKhxZdI81K25oM8gmERnioSSdh9iuv0vjmREgCRbiy8r74WXotHr4O35waOBittPOzY3Q_8wYPiYyAunKlBbh295ELggk8jqRPftfgQ2zsfMTjrZH-YXD0wwdJJ2rG7wo25K5YgS-hm-p-LS2FqwXQ91u5HQELz49fdVoQUoN90pdlveWuW9HDDjtbxbUBki8edIrdV6C6fQ0rA1E0ElzrAx-qMqWAkxINv1LJl7UUPBQkSNaixJy_eAp3-iMnQwvSwqmQmse2uOYskX9Ft04K9bsbrhoGcNhsyGBQIf5UD9OuvlEB1ksVptk4IN8WjapmTJN4gea9IFH4Vmx2VIOCRPC0kRFRP-ia383Q8LwW9DPHMSZkRqegny7b3A0XosrAURFTjr1AgEF73aXpcrWIzX_f6Xw1IRkRs2tp0OTXxdx_8VFX2oMRGt8kSg6lbuZyNJ08LK5i4q6PUkyQ3&response_mode=form_post&nonce=638729619076581239.MzI2NjdmZjktZGMzOC00NDMzLWIzNjctZGM2ZDk0ZTEyMWRlNjliYWNkN2YtYzBjNS00MDc5LWIzOTQtOGVkNGFmMGJhNDI5&code_challenge=UMUyHY-guXMrUIT13TLHAnhjDAO0nZPIZLusPUnLGFg&code_challenge_method=S256&x-client-SKU=ID_NET6_0&x-client-Ver=8.1.0.0&uaid=550bed0a33eb420bbc27778898d9332a&msproxy=1&issuer=mso&tenant=consumers&ui_locales=en-IN&client_info=1&epct=PAQABDgEAAABVrSpeuWamRam2jAF1XRQERjrsj7RynFvC5_IfzZqUCtDxodorVkPNtymgDnENBVKevVs9PHNq2G0C2qDNrLKy7u8tOrSsXpYJjMqaSqr-dkRRqC0cWLFxMlVqp_mhyldXBjlYiIy-aaFlBWS69r1bVF6gvt-rRN9lYDP0p_xAseDQ1XCLQ2Fls3N6nK_aZZDcWc1o6Yq9-aBwuxL7irAHDUFs3VplwARjiZl7Nvpt5yAA&jshs=0&claims=%7b%22compact%22%3a%7b%22name%22%3a%7b%22essential%22%3atrue%7d%7d%7d#"

#     for phone_number in phone_numbers:
#         # Setup Chrome driver with headless mode
#         chrome_options = Options()
#         chrome_options.add_argument("--headless")
#         chrome_options.add_argument("--disable-gpu")
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("--disable-dev-shm-usage")

#         driver = webdriver.Chrome(options=chrome_options)
#         wait = WebDriverWait(driver, 10)

#         try:
#             # Navigate to the login page
#             driver.get(base_url)
            
#             # Wait for the phone number input field
#             phone_input = wait.until(EC.presence_of_element_located((By.ID, "i0116")))
#             phone_input.clear()
#             phone_input.send_keys(str(phone_number))

#             # Click the Next button
#             next_button = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
#             next_button.click()

#             # Wait for a response
#             time.sleep(2)

#             # Try to capture the response message
#             try:
#                     page_text = driver.find_element(By.TAG_NAME, "body").text
#                     print(f"Phone number {phone_number}: Response - {page_text[:200]}...") 
#             except:
#                 try:
#                     response = driver.find_element(By.ID, "displayName").text
#                     print(f"Phone number {phone_number}: Account found - {response}")
#                 except:
#                     print(f"Phone number {phone_number}: Unable to determine response.")
#         except Exception as e:
#             print(f"Error processing phone number {phone_number}: {e}")
#         finally:
#             # Close the browser after processing each number
#             driver.quit()

# if __name__ == "__main__":
#     automate_login()


# # import os
# # import time
# # import logging
# # import threading
# # import queue
# # import psutil
# # from datetime import datetime
# # from concurrent.futures import ThreadPoolExecutor
# # from pathlib import Path
# # from selenium import webdriver
# # from selenium.webdriver.chrome.options import Options
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # import pandas as pd

# # # Create necessary directories
# # Path("logs").mkdir(exist_ok=True)
# # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# # # Configure logging
# # logging.basicConfig(level=logging.INFO)
# # event_logger = logging.getLogger('events')
# # perf_logger = logging.getLogger('performance')

# # # Add file handlers
# # event_handler = logging.FileHandler(f'logs/event_log_{timestamp}.log')
# # perf_handler = logging.FileHandler(f'logs/performance_log_{timestamp}.log')
# # event_logger.addHandler(event_handler)
# # perf_logger.addHandler(perf_handler)

# # class PerformanceMonitor(threading.Thread):
# #     def __init__(self, interval=1):
# #         super().__init__()
# #         self.interval = interval
# #         self._stop_event = threading.Event()

# #     def run(self):
# #         while not self._stop_event.is_set():
# #             cpu_usage = psutil.cpu_percent(interval=1)
# #             memory_usage = psutil.Process().memory_percent()
# #             perf_logger.info(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%")
# #             time.sleep(self.interval)

# #     def stop(self):
# #         self._stop_event.set()

# # def process_phone_number(phone_number):
# #     start_time = time.time()
# #     result = {"id": phone_number, "response": "", "duration": 0}
    
# #     chrome_options = Options()
# #     chrome_options.add_argument("--headless")
# #     chrome_options.add_argument("--disable-gpu")
# #     chrome_options.add_argument("--no-sandbox")
# #     chrome_options.add_argument("--disable-dev-shm-usage")

# #     driver = webdriver.Chrome(options=chrome_options)
# #     wait = WebDriverWait(driver, 10)

# #     try:
# #         # Shorter, more generic URL endpoint
# #         base_url = "https://login.live.com/oauth20/authorize"
# #         params = {
# #             "client_id": "10fa57ef-4895-4ab2-872c-8c3613d4f7fb",
# #             "response_type": "code",
# #             "redirect_uri": "https://www.microsoft.com/signin"
# #         }
        
# #         # Construct URL with parameters
# #         url = f"{base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"
        
# #         driver.get(url)
# #         event_logger.info(f"Processing phone number: {phone_number}")

# #         phone_input = wait.until(EC.presence_of_element_located((By.ID, "i0116")))
# #         phone_input.clear()
# #         phone_input.send_keys(str(phone_number))

# #         next_button = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
# #         next_button.click()

# #         time.sleep(2)

# #         try:
# #             page_text = driver.find_element(By.TAG_NAME, "body").text
# #             result["response"] = page_text[:200]
# #         except:
# #             try:
# #                 response = driver.find_element(By.ID, "displayName").text
# #                 result["response"] = f"Account found - {response}"
# #             except:
# #                 result["response"] = "Unable to determine response"

# #     except Exception as e:
# #         error_msg = f"Error processing phone number {phone_number}: {str(e)}"
# #         event_logger.error(error_msg)
# #         result["response"] = error_msg
# #     finally:
# #         driver.quit()
# #         result["duration"] = round(time.time() - start_time, 2)
# #         return result

# # def main():
# #     try:
# #         # Start performance monitoring
# #         perf_monitor = PerformanceMonitor()
# #         perf_monitor.start()

# #         # Read input file
# #         df = pd.read_excel('newest_file.xlsx')
# #         phone_numbers = df.iloc[:, 1].tolist()
        
# #         results = []
# #         max_workers = min(os.cpu_count() * 2, len(phone_numbers))  # Optimal number of workers

# #         # Process phone numbers using thread pool
# #         with ThreadPoolExecutor(max_workers=max_workers) as executor:
# #             futures = [executor.submit(process_phone_number, phone) for phone in phone_numbers]
# #             for future in futures:
# #                 result = future.result()
# #                 results.append(result)

# #         # Create results DataFrame and save to Excel
# #         results_df = pd.DataFrame(results)
# #         output_file = f'results_{timestamp}.xlsx'
# #         results_df.to_excel(output_file, index=False)
# #         event_logger.info(f"Results saved to {output_file}")

# #     except Exception as e:
# #         event_logger.error(f"Main process error: {str(e)}")
# #     finally:
# #         # Stop performance monitoring
# #         perf_monitor.stop()
# #         perf_monitor.join()

# # if __name__ == "__main__":
# #     main()


# # import time
# # import redis
# # from selenium import webdriver
# # from selenium.webdriver.chrome.options import Options
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC

# # # Redis client configuration
# # redis_client = redis.Redis(
# #     host='redis-19800.crce179.ap-south-1-1.ec2.redns.redis-cloud.com',
# #     port=19800,
# #     decode_responses=True,
# #     username="default",
# #     password="JMPog04EGI2MVcbO3HDPC9clDNyztfBX",
# # )

# # # Configuration for Redis keys
# # CONFIG = {
# #     "input_queue": "phone_numbers_input",  # Redis list for phone numbers
# #     "output_queue": "phone_numbers_output",  # Redis list for processed results
# #     "batch_size": 20  # Batch size for processing
# # }

# # # Base URL for login page
# # base_url = "https://login.live.com/oauth20_authorize.srf?client_id=10fa57ef-4895-4ab2-872c-8c3613d4f7fb&scope=openid+profile+offline_access&redirect_uri=https%3a%2f%2fwww.microsoft.com%2fcascadeauth%2faccount%2fsignin-oidc&response_type=code&state=CfDJ8P_pstto1o1NgBRsh8q_VvgvqWKhxZdI81K25oM8gmERnioSSdh9iuv0vjmREgCRbiy8r74WXotHr4O35waOBittPOzY3Q_8wYPiYyAunKlBbh295ELggk8jqRPftfgQ2zsfMTjrZH-YXD0wwdJJ2rG7wo25K5YgS-hm-p-LS2FqwXQ91u5HQELz49fdVoQUoN90pdlveWuW9HDDjtbxbUBki8edIrdV6C6fQ0rA1E0ElzrAx-qMqWAkxINv1LJl7UUPBQkSNaixJy_eAp3-iMnQwvSwqmQmse2uOYskX9Ft04K9bsbrhoGcNhsyGBQIf5UD9OuvlEB1ksVptk4IN8WjapmTJN4gea9IFH4Vmx2VIOCRPC0kRFRP-ia383Q8LwW9DPHMSZkRqegny7b3A0XosrAURFTjr1AgEF73aXpcrWIzX_f6Xw1IRkRs2tp0OTXxdx_8VFX2oMRGt8kSg6lbuZyNJ08LK5i4q6PUkyQ3&response_mode=form_post&nonce=638729619076581239.MzI2NjdmZjktZGMzOC00NDMzLWIzNjctZGM2ZDk0ZTEyMWRlNjliYWNkN2YtYzBjNS00MDc5LWIzOTQtOGVkNGFmMGJhNDI5&code_challenge=UMUyHY-guXMrUIT13TLHAnhjDAO0nZPIZLusPUnLGFg&code_challenge_method=S256&x-client-SKU=ID_NET6_0&x-client-Ver=8.1.0.0&uaid=550bed0a33eb420bbc27778898d9332a&msproxy=1&issuer=mso&tenant=consumers&ui_locales=en-IN&client_info=1&epct=PAQABDgEAAABVrSpeuWamRam2jAF1XRQERjrsj7RynFvC5_IfzZqUCtDxodorVkPNtymgDnENBVKevVs9PHNq2G0C2qDNrLKy7u8tOrSsXpYJjMqaSqr-dkRRqC0cWLFxMlVqp_mhyldXBjlYiIy-aaFlBWS69r1bVF6gvt-rRN9lYDP0p_xAseDQ1XCLQ2Fls3N6nK_aZZDcWc1o6Yq9-aBwuxL7irAHDUFs3VplwARjiZl7Nvpt5yAA&jshs=0&claims=%7b%22compact%22%3a%7b%22name%22%3a%7b%22essential%22%3atrue%7d%7d%7d#"

# # # Function to automate login process
# # def automate_login():
# #     try:
# #         while True:
# #             # Fetch a batch of phone numbers from Redis input queue
# #             phone_numbers = redis_client.lrange(CONFIG["input_queue"], 0, CONFIG["batch_size"] - 1)
# #             if not phone_numbers:
# #                 print("No more phone numbers to process.")
# #                 break

# #             # Process each phone number
# #             for phone_number in phone_numbers:
# #                 phone_number = phone_number.strip()  # Clean up phone number

# #                 # Setup Chrome driver with headless mode
# #                 chrome_options = Options()
# #                 chrome_options.add_argument("--headless")
# #                 chrome_options.add_argument("--disable-gpu")
# #                 chrome_options.add_argument("--no-sandbox")
# #                 chrome_options.add_argument("--disable-dev-shm-usage")

# #                 driver = webdriver.Chrome(options=chrome_options)
# #                 wait = WebDriverWait(driver, 10)

# #                 try:
# #                     # Navigate to the login page
# #                     driver.get(base_url)

# #                     # Wait for the phone number input field
# #                     phone_input = wait.until(EC.presence_of_element_located((By.ID, "i0116")))

# #                     # Enter the phone number and submit
# #                     phone_input.clear()
# #                     phone_input.send_keys(str(phone_number))

# #                     # Click the Next button
# #                     next_button = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
# #                     next_button.click()

# #                     # Wait for a response
# #                     time.sleep(2)

# #                     # Try to capture the response message
# #                     try:
# #                         page_text = driver.find_element(By.TAG_NAME, "body").text
# #                         print(f"Phone number {phone_number}: Response - {page_text[:200]}...")
# #                     except:
# #                         try:
# #                             response = driver.find_element(By.ID, "displayName").text
# #                             print(f"Phone number {phone_number}: Account found - {response}")
# #                         except:
# #                             print(f"Phone number {phone_number}: Unable to determine response.")

# #                     # Store the result in Redis output queue
# #                     redis_client.rpush(CONFIG["output_queue"], f"Phone number {phone_number}: Processed")

# #                 except Exception as e:
# #                     print(f"Error processing phone number {phone_number}: {e}")
# #                 finally:
# #                     # Close the browser after processing each number
# #                     driver.quit()

# #     except Exception as e:
# #         print(f"Error during execution: {e}")

# # if __name__ == "__main__":
# #     automate_login()


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os
import csv
from datetime import datetime
import logging

def setup_logging():
    # Create logs directory if it doesn't exist
    log_dir = 'logs-for-ms-phone'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Set up event logging
    event_logger = logging.getLogger('events')
    event_logger.setLevel(logging.INFO)
    event_handler = logging.FileHandler(os.path.join(log_dir, 'events.txt'))
    event_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    event_logger.addHandler(event_handler)
    
    # Set up performance logging
    perf_logger = logging.getLogger('performance')
    perf_logger.setLevel(logging.INFO)
    perf_handler = logging.FileHandler(os.path.join(log_dir, 'performance.txt'))
    perf_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    perf_logger.addHandler(perf_handler)
    
    return event_logger, perf_logger

def automate_login():
    # Set up logging
    event_logger, perf_logger = setup_logging()
    
    # Create timestamp for results file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f'results_{timestamp}.csv'
    
    # Create CSV file with headers
    with open(results_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Phone Number', 'Status', 'Response', 'Processing Time'])
    
    # Record start time
    total_start_time = time.time()
    
    # Read the Excel file
    try:
        df = pd.read_excel('newest_file.xlsx')
        phone_numbers = df.iloc[:, 1]  # Get the second column
        event_logger.info(f"Successfully loaded {len(phone_numbers)} phone numbers from Excel file")
    except Exception as e:
        event_logger.error(f"Error reading Excel file: {e}")
        return

    base_url = "https://login.live.com/oauth20_authorize.srf?client_id=10fa57ef-4895-4ab2-872c-8c3613d4f7fb&scope=openid+profile+offline_access&redirect_uri=https%3a%2f%2fwww.microsoft.com%2fcascadeauth%2faccount%2fsignin-oidc&response_type=code&state=CfDJ8P_pstto1o1NgBRsh8q_VvgvqWKhxZdI81K25oM8gmERnioSSdh9iuv0vjmREgCRbiy8r74WXotHr4O35waOBittPOzY3Q_8wYPiYyAunKlBbh295ELggk8jqRPftfgQ2zsfMTjrZH-YXD0wwdJJ2rG7wo25K5YgS-hm-p-LS2FqwXQ91u5HQELz49fdVoQUoN90pdlveWuW9HDDjtbxbUBki8edIrdV6C6fQ0rA1E0ElzrAx-qMqWAkxINv1LJl7UUPBQkSNaixJy_eAp3-iMnQwvSwqmQmse2uOYskX9Ft04K9bsbrhoGcNhsyGBQIf5UD9OuvlEB1ksVptk4IN8WjapmTJN4gea9IFH4Vmx2VIOCRPC0kRFRP-ia383Q8LwW9DPHMSZkRqegny7b3A0XosrAURFTjr1AgEF73aXpcrWIzX_f6Xw1IRkRs2tp0OTXxdx_8VFX2oMRGt8kSg6lbuZyNJ08LK5i4q6PUkyQ3&response_mode=form_post&nonce=638729619076581239.MzI2NjdmZjktZGMzOC00NDMzLWIzNjctZGM2ZDk0ZTEyMWRlNjliYWNkN2YtYzBjNS00MDc5LWIzOTQtOGVkNGFmMGJhNDI5&code_challenge=UMUyHY-guXMrUIT13TLHAnhjDAO0nZPIZLusPUnLGFg&code_challenge_method=S256&x-client-SKU=ID_NET6_0&x-client-Ver=8.1.0.0&uaid=550bed0a33eb420bbc27778898d9332a&msproxy=1&issuer=mso&tenant=consumers&ui_locales=en-IN&client_info=1&epct=PAQABDgEAAABVrSpeuWamRam2jAF1XRQERjrsj7RynFvC5_IfzZqUCtDxodorVkPNtymgDnENBVKevVs9PHNq2G0C2qDNrLKy7u8tOrSsXpYJjMqaSqr-dkRRqC0cWLFxMlVqp_mhyldXBjlYiIy-aaFlBWS69r1bVF6gvt-rRN9lYDP0p_xAseDQ1XCLQ2Fls3N6nK_aZZDcWc1o6Yq9-aBwuxL7irAHDUFs3VplwARjiZl7Nvpt5yAA&jshs=0&claims=%7b%22compact%22%3a%7b%22name%22%3a%7b%22essential%22%3atrue%7d%7d%7d#"

    for index, phone_number in enumerate(phone_numbers, 1):
        # Record start time for this phone number
        start_time = time.time()
        
        event_logger.info(f"Processing number {index}/{len(phone_numbers)}: {phone_number}")
        
        # Setup Chrome driver with headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 10)

        try:
            # Navigate to the login page
            driver.get(base_url)
            
            # Wait for the phone number input field
            phone_input = wait.until(EC.presence_of_element_located((By.ID, "i0116")))
            phone_input.clear()
            phone_input.send_keys(str(phone_number))

            # Click the Next button
            next_button = wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
            next_button.click()

            # Wait for a response
            time.sleep(2)

            # Try to capture the response message
            status = "Unknown"
            response_text = "Unable to determine response"
            
            try:
                page_text = driver.find_element(By.TAG_NAME, "body").text
                status = "Processed"
                response_text = page_text[:200]
                event_logger.info(f"Response received for {phone_number}: {response_text[:100]}...")
            except:
                try:
                    response_text = driver.find_element(By.ID, "displayName").text
                    status = "Account Found"
                    event_logger.info(f"Account found for {phone_number}: {response_text}")
                except:
                    status = "No Response"
                    event_logger.warning(f"Unable to determine response for {phone_number}")
                    
        except Exception as e:
            status = "Error"
            response_text = str(e)
            event_logger.error(f"Error processing {phone_number}: {e}")
        finally:
            # Calculate processing time
            processing_time = time.time() - start_time
            perf_logger.info(f"Phone {phone_number} - Processing time: {processing_time:.2f} seconds")
            
            # Save results to CSV
            with open(results_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([phone_number, status, response_text, f"{processing_time:.2f}s"])
            
            # Close the browser
            driver.quit()

    # Log total execution time
    total_time = time.time() - total_start_time
    event_logger.info(f"Total execution time: {total_time:.2f} seconds")
    perf_logger.info(f"Total execution time: {total_time:.2f} seconds")

if __name__ == "__main__":
    automate_login()