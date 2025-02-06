# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.common.keys import Keys
# # from selenium.webdriver.support import expected_conditions as EC
# # from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
# # from selenium.webdriver.common.action_chains import ActionChains
# # import time
# # import json
# # import os
# # from datetime import datetime
import random

import psutil
import redis
# # class SkypeAutomation:

# #     def __init__(self):
# #         self.driver = webdriver.Chrome()
# #         self.search_history = []
# #         self.load_search_history()

# #     def load_search_history(self):
# #         try:
# #             if os.path.exists('search_history.json'):
# #                 with open('search_history.json', 'r') as f:
# #                     self.search_history = json.load(f)
# #         except Exception as e:
# #             print(f"Error loading search history: {e}")
# #             self.search_history = []

# #     def save_search_history(self):
# #         try:
# #             with open('search_history.json', 'w') as f:
# #                 json.dump(self.search_history, f, indent=2)
# #         except Exception as e:
# #             print(f"Error saving search history: {e}")

# #     def handle_popups(self):
# #             try:
# #                 customize_profile = self.driver.find_element(By.XPATH, 
# #                     "//div[contains(text(), 'Customize your profile')]")
# #                 if customize_profile:
# #                     try:
# #                         close_button = self.driver.find_element(By.XPATH, 
# #                             "//button[contains(@aria-label, 'Close')]")
# #                         close_button.click()
# #                     except:
# #                         ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
# #                     time.sleep(1)
# #             except:
# #                 pass

# #     def get_search_results(self):
# #         try:
# #             # Wait for results to load
# #             time.sleep(3)

# #             # Find all result containers
# #             results = self.driver.find_elements(By.XPATH, 
# #                 "//div[contains(@class, 'search-result') or contains(@class, 'search-item')]")

# #             if not results:
# #                 # Try alternative selector
# #                 results = self.driver.find_elements(By.XPATH, 
# #                     "//div[contains(@role, 'listitem')]")

# #             search_results = []
# #             for result in results:
# #                 try:
# #                     # Try to get name/title
# #                     name = result.find_element(By.XPATH, 
# #                         ".//div[contains(@class, 'title') or contains(@class, 'name')]").text
# #                 except:
# #                     try:
# #                         # Fallback to any text content
# #                         name = result.text
# #                     except:
# #                         name = "Unknown"

# #                 if name and name.strip():
# #                     search_results.append(name.strip())

# #             return search_results
# #         except Exception as e:
# #             print(f"Error getting search results: {e}")
# #             return []

# #     def search_contact(self, search_term):
# #         try:
# #             # Wait for page to fully load
# #             time.sleep(5)

# #             # Handle any popups first
# #             self.handle_popups()

# #             # Try multiple methods to initiate search
# #             try:
# #                 search_div = WebDriverWait(self.driver, 10).until(
# #                     EC.element_to_be_clickable((By.XPATH, 
# #                     "//div[@aria-label='People, groups, messages' and @role='button']"))
# #                 )
# #                 search_div.click()
# #             except ElementClickInterceptedException:
# #                 try:
# #                     search_div = self.driver.find_element(By.XPATH, 
# #                         "//div[@aria-label='People, groups, messages' and @role='button']")
# #                     self.driver.execute_script("arguments[0].click();", search_div)
# #                 except:
# #                     ActionChains(self.driver).send_keys("/").perform()

# #             time.sleep(2)

# #             # Send search term
# #             actions = ActionChains(self.driver)
# #             actions.send_keys(search_term)
# #             actions.send_keys(Keys.RETURN)
# #             actions.perform()

# #             # Get search results
# #             results = self.get_search_results()

# #             # Create search record
# #             search_record = {
# #                 "search_term": search_term,
# #                 "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
# #                 "results": results
# #             }

# #             # Add to search history
# #             self.search_history.append(search_record)
# #             self.save_search_history()

# #             # Display results in terminal
# #             print("\nSearch Results for:", search_term)
# #             if results:
# #                 for idx, result in enumerate(results, 1):
# #                     print(f"{idx}. {result}")
# #             else:
# #                 print("No results found")

# #             # Display search history
# #             print("\nSearch History:")
# #             for idx, record in enumerate(self.search_history, 1):
# #                 print(f"{idx}. {record['search_term']} ({record['timestamp']})")
# #                 if record['results']:
# #                     for result in record['results']:
# #                         print(f"   - {result}")
# #                 else:
# #                     print("   No results")

# #             return True

# #         except Exception as e:
# #             print(f"Search failed: {e}")
# #             return False

# #     def wait_and_find_element(self, by, value, timeout=20):
# #         try:
# #             element = WebDriverWait(self.driver, timeout).until(
# #                 EC.presence_of_element_located((by, value))
# #             )
# #             time.sleep(1)
# #             return element
# #         except TimeoutException:
# #             print(f"Element not found: {value}")
# #             return None

# #     def wait_and_find_clickable(self, by, value, timeout=20):
# #         try:
# #             element = WebDriverWait(self.driver, timeout).until(
# #                 EC.element_to_be_clickable((by, value))
# #             )
# #             time.sleep(1)
# #             return element
# #         except TimeoutException:
# #             print(f"Clickable element not found: {value}")
# #             return None

# #     def login(self, email="aryapvt190@gmail.com", password="Arya2907#"):
# #         try:
# #             self.driver.get("https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=170&ct=1737458607&rver=7.5.2156.0&wp=MBI_SSL&wreply=https%3A%2F%2Flw.skype.com%2Flogin%2Foauth%2Fproxy%3Fclient_id%3D572381%26redirect_uri%3Dhttps%253A%252F%252Fweb.skype.com%252FAuth%252FPostHandler%26state%3Dc4408367-84ba-44af-929a-b7ddb9f75e49&lc=1033&id=293290&mkt=en-US&psi=skype&lw=1&cobrandid=2befc4b5-19e3-46e8-8347-77317a16a5a5&client_flight=ReservedFlight33%2CReservedFlight67")

# #             email_field = self.wait_and_find_element(By.NAME, "loginfmt")
# #             if email_field:
# #                 email_field.send_keys(email)
# #                 next_button = self.wait_and_find_element(By.ID, "idSIButton9")
# #                 if next_button:
# #                     next_button.click()

# #             password_field = self.wait_and_find_element(By.NAME, "passwd")
# #             if password_field:
# #                 password_field.send_keys(password)
# #                 sign_in_button = self.wait_and_find_element(By.ID, "idSIButton9")
# #                 if sign_in_button:
# #                     sign_in_button.click()

# #             stay_signed_in = self.wait_and_find_element(By.ID, "acceptButton")
# #             if stay_signed_in:
# #                 stay_signed_in.click()

# #             time.sleep(8)
# #             return True

# #         except Exception as e:
# #             print(f"Login failed: {e}")
# #             return False

# #     def close(self):
# #         self.driver.quit()

# # def main():
# #     bot = SkypeAutomation()

# #     if bot.login():
# #         print("Successfully logged in")

# #         while True:
# #             search_term = input("\nEnter email/phone to search (or 'quit' to exit): ")
# #             if search_term.lower() == 'quit':
# #                 break

# #             if bot.search_contact(search_term):
# #                 print(f"Successfully searched for: {search_term}")
# #             else:
# #                 print(f"Failed to search for: {search_term}")

# #     bot.close()

# # if __name__ == "__main__":
# #     main()

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.chrome.options import Options
# import time
# import json
# import os
# from datetime import datetime

# class SkypeAutomation:
#     def __init__(self):
#         chrome_options = Options()
#         chrome_options.add_argument("--start-maximized")
#         chrome_options.add_argument("--disable-notifications")
#         self.driver = webdriver.Chrome(options=chrome_options)
#         self.search_history = []
#         self.load_search_history()

#     def load_search_history(self):
#         try:
#             if os.path.exists('search_history.json'):
#                 with open('search_history.json', 'r') as f:
#                     self.search_history = json.load(f)
#         except Exception as e:
#             print(f"Error loading search history: {e}")
#             self.search_history = []

#     def save_search_history(self):
#         try:
#             with open('search_history.json', 'w') as f:
#                 json.dump(self.search_history, f, indent=2)
#         except Exception as e:
#             print(f"Error saving search history: {e}")

#     def handle_popups(self):
#         try:
#             customize_profile = self.driver.find_element(By.XPATH, 
#                 "//div[contains(text(), 'Customize your profile')]")
#             if customize_profile:
#                 try:
#                     close_button = self.driver.find_element(By.XPATH, 
#                         "//button[contains(@aria-label, 'Close')]")
#                     close_button.click()
#                 except:
#                     ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
#                 time.sleep(1)
#         except:
#             pass

#     def get_search_results(self):
#         results = []
#         max_retries = 3
#         retry_count = 0

#         while retry_count < max_retries:
#             try:
#                 # Wait for results to load
#                 time.sleep(3)

#                 # First try to find results with original selectors
#                 results = self.driver.find_elements(By.XPATH, 
#                     "//div[contains(@class, 'search-result') or contains(@class, 'search-item')]")

#                 if not results:
#                     # Try alternative selector
#                     results = self.driver.find_elements(By.XPATH, 
#                         "//div[contains(@role, 'listitem')]")

#                 search_results = []
#                 for result in results:
#                     try:
#                         # Try to get name/title
#                         name = result.find_element(By.XPATH, 
#                             ".//div[contains(@class, 'title') or contains(@class, 'name')]").text
#                     except:
#                         try:
#                             # Fallback to any text content
#                             name = result.text
#                         except:
#                             continue

#                     if name and name.strip():
#                         search_results.append(name.strip())

#                 if search_results:
#                     return search_results

#                 retry_count += 1
#                 time.sleep(2)

#             except (TimeoutException, StaleElementReferenceException) as e:
#                 print(f"Attempt {retry_count + 1} failed: {str(e)}")
#                 retry_count += 1
#                 time.sleep(2)

#         return []

#     def search_contact(self, search_term):
#         try:
#             # Wait for page to load
#             time.sleep(5)

#             # Handle any popups
#             self.handle_popups()

#             # Clear previous search if any
#             ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
#             time.sleep(2)

#             # Try to click search using original selector

#             try:
#                 search_div = WebDriverWait(self.driver, 10).until(
#                     EC.element_to_be_clickable((By.XPATH, 
#                     "//div[@aria-label='People, groups, messages' and @role='button']"))
#                 )
#                 search_div.click()
#             except ElementClickInterceptedException:
#                 try:
#                     search_div = self.driver.find_element(By.XPATH, 
#                         "//div[@aria-label='People, groups, messages' and @role='button']")
#                     self.driver.execute_script("arguments[0].click();", search_div)
#                 except:
#                     ActionChains(self.driver).send_keys("/").perform()

#             time.sleep(2)

#             # Clear any existing search text and enter new search
#             actions = ActionChains(self.driver)
#             actions.send_keys(search_term)
#             actions.send_keys(Keys.RETURN)
#             actions.perform()

#             # Get search results
#             results = self.get_search_results()

#             # Create search record
#             search_record = {
#                 "search_term": search_term,
#                 "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                 "results": results
#             }

#             # Add to search history
#             self.search_history.append(search_record)
#             self.save_search_history()

#             # Display results
#             print("\nSearch Results for:", search_term)
#             if results:
#                 for idx, result in enumerate(results, 1):
#                     print(f"{idx}. {result}")
#             else:
#                 print("No results found")

#             # Display search history
#             print("\nSearch History:")
#             for idx, record in enumerate(self.search_history, 1):
#                 print(f"{idx}. {record['search_term']} ({record['timestamp']})")
#                 if record['results']:
#                     for result in record['results']:
#                         print(f"   - {result}")
#                 else:
#                     print("   No results")

#             return True

#         except Exception as e:
#             print(f"Search failed: {str(e)}")
#             return False

#     def search_contact_second(self, search_term):
#         try:
#             # Wait for page to load
#             time.sleep(5)

#             # Handle any popups
#             self.handle_popups()

#             # Clear previous search if any
#             ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
#             time.sleep(2)

#             # Clear any existing search text and enter new search
#             actions = ActionChains(self.driver)
#             actions.send_keys(search_term)
#             actions.send_keys(Keys.RETURN)
#             actions.perform()

#             # Get search results
#             results = self.get_search_results()

#             # Create search record
#             search_record = {
#                 "search_term": search_term,
#                 "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                 "results": results
#             }

#             # Add to search history
#             self.search_history.append(search_record)
#             self.save_search_history()

#             # Display results
#             print("\nSearch Results for:", search_term)
#             if results:
#                 for idx, result in enumerate(results, 1):
#                     print(f"{idx}. {result}")
#             else:
#                 print("No results found")

#             # Display search history
#             print("\nSearch History:")
#             for idx, record in enumerate(self.search_history, 1):
#                 print(f"{idx}. {record['search_term']} ({record['timestamp']})")
#                 if record['results']:
#                     for result in record['results']:
#                         print(f"   - {result}")
#                 else:
#                     print("   No results")

#             return True

#         except Exception as e:
#             print(f"Search failed: {str(e)}")
#             return False

#     def wait_and_find_element(self, by, value, timeout=20):
#         try:
#             element = WebDriverWait(self.driver, timeout).until(
#                 EC.presence_of_element_located((by, value))
#             )
#             time.sleep(1)
#             return element
#         except TimeoutException:
#             print(f"Element not found: {value}")
#             return None

#     def login(self, email="aryapvt190@gmail.com", password="Arya2907#"):
#         try:
#             self.driver.get("https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=170&ct=1737458607&rver=7.5.2156.0&wp=MBI_SSL&wreply=https%3A%2F%2Flw.skype.com%2Flogin%2Foauth%2Fproxy%3Fclient_id%3D572381%26redirect_uri%3Dhttps%253A%252F%252Fweb.skype.com%252FAuth%252FPostHandler%26state%3Dc4408367-84ba-44af-929a-b7ddb9f75e49&lc=1033&id=293290&mkt=en-US&psi=skype&lw=1&cobrandid=2befc4b5-19e3-46e8-8347-77317a16a5a5&client_flight=ReservedFlight33%2CReservedFlight67")

#             email_field = self.wait_and_find_element(By.NAME, "loginfmt")
#             if email_field:
#                 email_field.send_keys(email)
#                 next_button = self.wait_and_find_element(By.ID, "idSIButton9")
#                 if next_button:
#                     next_button.click()

#             password_field = self.wait_and_find_element(By.NAME, "passwd")
#             if password_field:
#                 password_field.send_keys(password)
#                 sign_in_button = self.wait_and_find_element(By.ID, "idSIButton9")
#                 if sign_in_button:
#                     sign_in_button.click()

#             stay_signed_in = self.wait_and_find_element(By.ID, "acceptButton")
#             if stay_signed_in:
#                 stay_signed_in.click()

#             time.sleep(8)
#             return True

#         except Exception as e:
#             print(f"Login failed: {str(e)}")
#             return False

#     def close(self):
#         try:
#             self.driver.quit()
#         except Exception as e:
#             print(f"Error closing browser: {str(e)}")

# def main():
#     bot = SkypeAutomation()

#     if bot.login():
#         print("Successfully logged in")
#         i = 0
#         while True:
#             search_term = input("\nEnter email/phone to search (or 'quit' to exit): ")
#             if search_term.lower() == 'quit':
#                 break

#             if i == 0:    
#                 if bot.search_contact(search_term):
#                     print(f"Successfully searched for: {search_term}")
#                     i+=1
#                 else:
#                     print(f"Failed to search for: {search_term}")
#             else:
#                 if bot.search_contact_second(search_term):
#                     print(f"Successfully searched for: {search_term}")
#                 else:
#                     print(f"Failed to search for: {search_term}") 
#     bot.close()

# if __name__ == "__main__":
#     main()

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.chrome.options import Options
# import json
# import os
# import pandas as pd
# from datetime import datetime
# import psutil
# import logging
# from logging.handlers import RotatingFileHandler
# import sys
# import time

# class SkypeAutomation:
#     def __init__(self):
#         # Set up logging
#         self.setup_logging()

#         # Initialize Chrome in headless mode
#         self.logger.info("Initializing Chrome in headless mode")
#         chrome_options = Options()
#         chrome_options.add_argument("--headless=new")
#         chrome_options.add_argument("--disable-gpu")
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("--disable-dev-shm-usage")
#         chrome_options.add_argument("--window-size=1920,1080")
#         chrome_options.add_argument("--disable-notifications")
#         chrome_options.add_argument("--disable-popup-blocking")
#         chrome_options.add_argument('--enable-unsafe-swiftshader')  # Added to handle WebGL warning

#         self.driver = webdriver.Chrome(options=chrome_options)
#         self.search_div = None
#         self.search_history = []
#         self.load_search_history()

#         # Initialize performance logging
#         self.perf_logger = self.setup_performance_logging()
#         self.process = psutil.Process()
#         self.log_performance("Initialization")

#     # [Previous logging setup methods remain the same]
#     def setup_logging(self):
#         os.makedirs('logs-ms-phone', exist_ok=True)
#         self.logger = logging.getLogger('event_logger')
#         self.logger.setLevel(logging.INFO)
#         formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

#         file_handler = RotatingFileHandler(
#             'logs-ms-phone/event_logs.txt',
#             maxBytes=10485760,
#             backupCount=5
#         )
#         file_handler.setFormatter(formatter)
#         self.logger.addHandler(file_handler)

#         console_handler = logging.StreamHandler(sys.stdout)
#         console_handler.setFormatter(formatter)
#         self.logger.addHandler(console_handler)

#     def setup_performance_logging(self):
#         perf_logger = logging.getLogger('performance_logger')
#         perf_logger.setLevel(logging.INFO)
#         formatter = logging.Formatter('%(asctime)s - %(message)s')

#         file_handler = RotatingFileHandler(
#             'logs-ms-phone/performance_logs.txt',
#             maxBytes=10485760,
#             backupCount=5
#         )
#         file_handler.setFormatter(formatter)
#         perf_logger.addHandler(file_handler)
#         return perf_logger

#     def log_performance(self, operation):
#         cpu_percent = self.process.cpu_percent()
#         memory_info = self.process.memory_info()
#         memory_mb = memory_info.rss / 1024 / 1024
#         self.perf_logger.info(
#             f"Operation: {operation} | CPU: {cpu_percent}% | Memory: {memory_mb:.2f}MB"
#         )

#     def load_search_history(self):
#         try:
#             if os.path.exists('search_history.json'):
#                 with open('search_history.json', 'r') as f:
#                     self.search_history = json.load(f)
#                 self.logger.info("Search history loaded successfully")
#         except Exception as e:
#             self.logger.error(f"Error loading search history: {e}")
#             self.search_history = []

#     def save_search_history(self):
#         try:
#             with open('search_history.json', 'w') as f:
#                 json.dump(self.search_history, f, indent=2)
#             self.logger.info("Search history saved successfully")
#         except Exception as e:
#             self.logger.error(f"Error saving search history: {e}")

#     def handle_popups(self):
#         try:
#             customize_profile = self.driver.find_element(By.XPATH, 
#                 "//div[contains(text(), 'Customize your profile')]")
#             if customize_profile:
#                 close_button = self.driver.find_element(By.XPATH, 
#                     "//button[contains(@aria-label, 'Close')]")
#                 close_button.click() if close_button else ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
#                 self.logger.info("Popup handled successfully")
#         except:
#             pass

#     def get_search_results(self):
#         try:
#             results = self.driver.find_elements(By.XPATH, 
#                 "//div[contains(@class, 'search-result') or contains(@class, 'search-item')]")

#             if not results:
#                 results = self.driver.find_elements(By.XPATH, 
#                     "//div[contains(@role, 'listitem')]")

#             search_results = []
#             for result in results:
#                 try:
#                     name = result.find_element(By.XPATH, 
#                         ".//div[contains(@class, 'title') or contains(@class, 'name')]").text
#                 except:
#                     try:
#                         name = result.text
#                     except:
#                         continue

#                 if name and name.strip():
#                     search_results.append(name.strip())

#             self.logger.info(f"Found {len(search_results)} search results")
#             return search_results

#         except Exception as e:
#             self.logger.error(f"Error getting search results: {e}")
#             return []


#     def initialize_search(self):
#         self.logger.info("Attempting to initialize search")
#         try:
#             # Wait for Skype to fully load
#             time.sleep(5)
#             self.handle_popups()

#             # Try multiple approaches to find and click the search element
#             try:
#                 search_div = WebDriverWait(self.driver, 20).until(
#                     EC.presence_of_element_located((By.XPATH, 
#                     "//div[@aria-label='People, groups, messages' and @role='button']"))
#                 )

#                 try:
#                     search_div.click()
#                 except ElementClickInterceptedException:
#                     self.driver.execute_script("arguments[0].click();", search_div)

#                 self.search_div = search_div
#                 self.logger.info("Search initialized successfully using main selector")
#                 return True

#             except:
#                 # Fallback to keyboard shortcut
#                 self.logger.info("Trying keyboard shortcut for search")
#                 ActionChains(self.driver).send_keys("/").perform()
#                 time.sleep(2)
#                 return True

#         except Exception as e:
#             self.logger.error(f"Failed to initialize search: {e}")
#             return False

#     def search_contact(self, search_term):
#         self.logger.info(f"Searching for contact: {search_term}")
#         self.log_performance(f"Search start - {search_term}")

#         try:
#             # Clear previous search
#             ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()

#             # Wait briefly for the escape key to take effect
#             time.sleep(1)

#             # Try to click search div if it exists
#             if self.search_div:
#                 try:
#                     self.search_div.click()
#                 except:
#                     try:
#                         self.driver.execute_script("arguments[0].click();", self.search_div)
#                     except:
#                         ActionChains(self.driver).send_keys("/").perform()

#             # Enter search term
#             actions = ActionChains(self.driver)
#             actions.send_keys(search_term)
#             actions.send_keys(Keys.RETURN)
#             actions.perform()

#             # Wait for results
#             time.sleep(3)

#             # Get results
#             results = self.get_search_results()

#             # Log results
#             if results:
#                 self.logger.info(f"Found {len(results)} results for {search_term}")
#             else:
#                 self.logger.info(f"No results found for {search_term}")

#             # Create search record
#             search_record = {
#                 "search_term": search_term,
#                 "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                 "results": results
#             }

#             self.search_history.append(search_record)
#             self.save_search_history()

#             self.log_performance(f"Search complete - {search_term}")
#             return results

#         except Exception as e:
#             self.logger.error(f"Search failed for {search_term}: {e}")
#             self.log_performance(f"Search failed - {search_term}")
#             return []

#     def get_search_results(self):
#         try:
#             # Wait for results container
#             time.sleep(3)

#             # Try multiple selectors for results
#             results = self.driver.find_elements(By.XPATH, 
#                 "//div[contains(@class, 'search-result') or contains(@class, 'search-item')]")

#             if not results:
#                 results = self.driver.find_elements(By.XPATH, 
#                     "//div[contains(@role, 'listitem')]")

#             search_results = []
#             for result in results:
#                 try:
#                     name = result.find_element(By.XPATH, 
#                         ".//div[contains(@class, 'title') or contains(@class, 'name')]").text
#                 except:
#                     try:
#                         name = result.text
#                     except:
#                         continue

#                 if name and name.strip():
#                     search_results.append(name.strip())

#             return search_results

#         except Exception as e:
#             self.logger.error(f"Error getting search results: {e}")
#             return []

#     def wait_and_find_element(self, by, value, timeout=10):
#         try:
#             element = WebDriverWait(self.driver, timeout).until(
#                 EC.presence_of_element_located((by, value))
#             )
#             return element
#         except TimeoutException:
#             self.logger.error(f"Element not found: {value}")
#             return None

#     def login(self, email="aryapvt190@gmail.com", password="Arya2907#"):
#         self.logger.info("Attempting login")
#         self.log_performance("Login start")

#         try:
#             self.driver.get("https://web.skype.com")
#             time.sleep(3)  # Wait for redirect

#             # Handle login form
#             email_field = self.wait_and_find_element(By.NAME, "loginfmt", timeout=30)
#             if email_field:
#                 email_field.send_keys(email)
#                 next_button = self.wait_and_find_element(By.ID, "idSIButton9")
#                 if next_button:
#                     next_button.click()

#             password_field = self.wait_and_find_element(By.NAME, "passwd", timeout=30)
#             if password_field:
#                 password_field.send_keys(password)
#                 sign_in_button = self.wait_and_find_element(By.ID, "idSIButton9")
#                 if sign_in_button:
#                     sign_in_button.click()

#             # Handle "Stay signed in?" prompt
#             stay_signed_in = self.wait_and_find_element(By.ID, "acceptButton", timeout=30)
#             if stay_signed_in:
#                 stay_signed_in.click()

#             # Wait for Skype to load
#             time.sleep(10)

#             self.logger.info("Login successful")
#             self.log_performance("Login complete")
#             return True

#         except Exception as e:
#             self.logger.error(f"Login failed: {e}")
#             self.log_performance("Login failed")
#             return False


# def main():
#     try:
#         df = pd.read_excel('ms-phone.xlsx')
#         if len(df.columns) < 2:
#             print("Excel file must have at least 2 columns")
#             return
#     except Exception as e:
#         print(f"Error reading Excel file: {str(e)}")
#         return

#     bot = SkypeAutomation()
#     results_data = []

#     if bot.login():
#         if bot.initialize_search():
#             total_contacts = len(df)

#             for index, row in df.iterrows():
#                 contact = str(row[1])
#                 bot.logger.info(f"Processing contact {index + 1}/{total_contacts}: {contact}")

#                 results = bot.search_contact(contact)

#                 results_data.append({
#                     'Original': row[0],
#                     'Results': '\n'.join(results) if results else 'No results found'
#                 })

#                 # Small delay between searches
#                 time.sleep(2)

#     bot.close()

#     try:
#         results_df = pd.DataFrame(results_data)
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         output_filename = f'results_{timestamp}.xlsx'
#         results_df.to_excel(output_filename, index=False)
#         bot.logger.info(f"Results saved to {output_filename}")
#     except Exception as e:
#         bot.logger.error(f"Error saving results to Excel: {e}")

# if __name__ == "__main__":
#     main()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import json
import os
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import sys
import time
import concurrent.futures
import csv
from queue import Queue
from threading import Lock


class SkypeAutomation:
    def __init__(self, worker_id):
        self.worker_id = worker_id
        self.setup_logging()

        self.logger.info(f"Initializing Chrome for worker {worker_id}")
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument('--enable-unsafe-swiftshader')

        self.driver = webdriver.Chrome(options=chrome_options)
        self.search_div = None
        self.search_history = []
        self.load_search_history()

        self.perf_logger = self.setup_performance_logging()
        self.process = psutil.Process()
        self.log_performance("Initialization")

    def setup_logging(self):
        os.makedirs('logs-ms-phone', exist_ok=True)
        self.logger = logging.getLogger('event_logger')
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = RotatingFileHandler(
            'logs-ms-phone/event_logs.txt',
            maxBytes=10485760,
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def setup_performance_logging(self):
        perf_logger = logging.getLogger('performance_logger')
        perf_logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')

        file_handler = RotatingFileHandler(
            'logs-ms-phone/performance_logs.txt',
            maxBytes=10485760,
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        perf_logger.addHandler(file_handler)
        return perf_logger

    def log_performance(self, operation):
        cpu_percent = self.process.cpu_percent()
        memory_info = self.process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024
        self.perf_logger.info(
            f"Operation: {operation} | CPU: {cpu_percent}% | Memory: {memory_mb:.2f}MB"
        )

    def load_search_history(self):
        try:
            if os.path.exists('search_history.json'):
                with open('search_history.json', 'r') as f:
                    self.search_history = json.load(f)
                self.logger.info("Search history loaded successfully")
        except Exception as e:
            self.logger.error(f"Error loading search history: {e}")
            self.search_history = []

    def save_search_history(self):
        try:
            with open('search_history.json', 'w') as f:
                json.dump(self.search_history, f, indent=2)
            self.logger.info("Search history saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving search history: {e}")

    def handle_popups(self):
        try:
            customize_profile = self.driver.find_element(By.XPATH,
                                                         "//div[contains(text(), 'Customize your profile')]")
            if customize_profile:
                close_button = self.driver.find_element(By.XPATH,
                                                        "//button[contains(@aria-label, 'Close')]")
                close_button.click() if close_button else ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                self.logger.info("Popup handled successfully")
        except:
            pass

    def get_search_results(self):
        try:
            time.sleep(3)

            results = self.driver.find_elements(By.XPATH,
                                                "//div[contains(@class, 'search-result') or contains(@class, 'search-item')]")

            if not results:
                results = self.driver.find_elements(By.XPATH,
                                                    "//div[contains(@role, 'listitem')]")

            search_results = []
            for result in results:
                try:
                    name = result.find_element(By.XPATH,
                                               ".//div[contains(@class, 'title') or contains(@class, 'name')]").text
                except:
                    try:
                        name = result.text
                    except:
                        continue

                if name and name.strip():
                    search_results.append(name.strip())

            self.logger.info(f"Found {len(search_results)} search results")
            return search_results

        except Exception as e:
            self.logger.error(f"Error getting search results: {e}")
            return []

    def initialize_search(self):
        self.logger.info("Attempting to initialize search")
        try:
            time.sleep(5)
            self.handle_popups()

            try:
                search_div = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "//div[@aria-label='People, groups, messages' and @role='button']"))
                )

                try:
                    search_div.click()
                except ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click();", search_div)

                self.search_div = search_div
                self.logger.info("Search initialized successfully using main selector")
                return True

            except:
                self.logger.info("Trying keyboard shortcut for search")
                ActionChains(self.driver).send_keys("/").perform()
                time.sleep(2)
                return True

        except Exception as e:
            self.logger.error(f"Failed to initialize search: {e}")
            return False

    def search_contact(self, search_term):
        self.logger.info(f"Searching for contact: {search_term}")
        self.log_performance(f"Search start - {search_term}")

        try:
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(1)

            if self.search_div:
                try:
                    self.search_div.click()
                except:
                    try:
                        self.driver.execute_script("arguments[0].click();", self.search_div)
                    except:
                        ActionChains(self.driver).send_keys("/").perform()

            actions = ActionChains(self.driver)
            actions.send_keys(search_term)
            actions.send_keys(Keys.RETURN)
            actions.perform()

            time.sleep(3)
            results = self.get_search_results()

            if results:
                self.logger.info(f"Found {len(results)} results for {search_term}")
            else:
                self.logger.info(f"No results found for {search_term}")

            search_record = {
                "search_term": search_term,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "results": results
            }

            self.search_history.append(search_record)
            self.save_search_history()

            self.log_performance(f"Search complete - {search_term}")
            return results

        except Exception as e:
            self.logger.error(f"Search failed for {search_term}: {e}")
            self.log_performance(f"Search failed - {search_term}")
            return []

    def wait_and_find_element(self, by, value, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {value}")
            return None

    def login(self, email="aryapvt190@gmail.com", password="Arya2907#"):
        self.logger.info("Attempting login")
        self.log_performance("Login start")

        try:
            self.driver.get("https://web.skype.com")
            time.sleep(3)

            email_field = self.wait_and_find_element(By.NAME, "loginfmt", timeout=30)
            if email_field:
                email_field.send_keys(email)
                next_button = self.wait_and_find_element(By.ID, "idSIButton9")
                if next_button:
                    next_button.click()

            password_field = self.wait_and_find_element(By.NAME, "passwd", timeout=30)
            if password_field:
                password_field.send_keys(password)
                sign_in_button = self.wait_and_find_element(By.ID, "idSIButton9")
                if sign_in_button:
                    sign_in_button.click()

            stay_signed_in = self.wait_and_find_element(By.ID, "acceptButton", timeout=30)
            if stay_signed_in:
                stay_signed_in.click()

            time.sleep(10)

            self.logger.info("Login successful")
            self.log_performance("Login complete")
            return True

        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            self.log_performance("Login failed")
            return False

    def process_contact(self, email):
        """Process a single contact and return results"""
        try:
            if not hasattr(self, 'is_logged_in'):
                self.is_logged_in = self.login()
                if not self.is_logged_in:
                    return email, "Login failed"

                if not self.initialize_search():
                    return email, "Search initialization failed"

            results = self.search_contact(email)
            return email, '\n'.join(results) if results else 'No results found'

        except Exception as e:
            self.logger.error(f"Error processing contact {email}: {e}")
            return email, f"Error: {str(e)}"

    def close(self):
        try:
            self.driver.quit()
            self.logger.info(f"Browser closed for worker {self.worker_id}")
        except Exception as e:
            self.logger.error(f"Error closing browser for worker {self.worker_id}: {e}")


class ResultWriter:
    def __init__(self, output_file):
        self.output_file = output_file
        self.lock = Lock()
        self.initialize_csv()

    def initialize_csv(self):
        with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Email', 'Results'])

    def write_result(self, email, result):
        with self.lock:
            with open(self.output_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([email, result])


def process_batch(worker_id, emails, result_writer):
    bot = SkypeAutomation(worker_id)
    try:
        for email in emails:
            email, result = bot.process_contact(email)
            result_writer.write_result(email, result)
    finally:
        bot.close()


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


def main():
    try:
        # Read Excel file

        # Calculate optimal number of workers based on CPU cores
        bot = SkypeAutomation(1)
        while True:
            # Pull a phone number from the Redis list (blocking call)
            result = redis_client.brpop("skype", timeout=30)  # Adjust the timeout as needed
            if not result:
                print("No more emails to process. Exiting.")
                end_time = int(time.time() * 1000)
                print(f"Runtime: {end_time - start_time}ms")
                break

            email = result[1]  # Decode the number from bytes
            print(f"Processing email: {email}")
            email, result = bot.process_contact(email)
            redis_client.lpush("skype_results", f"{scrapper_id},{email},{result},{int(time.time() * 1000)}")

    except Exception as e:
        print(f"Error in main execution: {str(e)}")


if __name__ == "__main__":
    main()
