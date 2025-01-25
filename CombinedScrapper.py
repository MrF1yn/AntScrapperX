# import pandas as pd
# import re
# import asyncio
# import aiohttp
# import json
# from datetime import datetime

# proxies = {
#     "http": "geonode_1VvZ28sUKX:3860618c-044d-4622-af4e-95200f09ce05@92.204.164.15:9000",
#     "https": "geonode_1VvZ28sUKX:3860618c-044d-4622-af4e-95200f09ce05@92.204.164.15:9000",
# }

# def validate_and_format_mobile(row):
#     uid, mobile = row['UID'], str(row['Mobile'])

#     if pd.isna(mobile) or mobile.strip() == "":
#         return f"Invalid mobile number format for UID {uid}: {mobile}", None

#     mobile = re.sub(r'\D', '', mobile)

#     if len(mobile) == 10:
#         mobile = "91" + mobile
#     elif len(mobile) == 12 and mobile.startswith("91"):
#         pass
#     else:
#         return f"Invalid mobile number format for UID {uid}: {mobile}", None

#     return f"Valid mobile number for UID {uid}: {mobile}", mobile

# async def check_toi(session, mobile):
#     try:
#         url = "https://jsso.indiatimes.com/sso/crossapp/identity/web/checkUserExists"
#         headers = {
#             "Content-Type": "application/json",
#             "Accept": "*/*",
#             "Referer": "https://timesofindia.indiatimes.com/",
#             "Origin": "https://timesofindia.indiatimes.com",
#             "channel": "toi",
#             "sdkversion": "0.7.993"
#         }
#         payload = {"identifier": mobile}
#         async with session.post(url, headers=headers, json=payload) as response:
#             if response.status == 200:
#                 response_data = await response.json()
#                 status_code = response_data.get("data", {}).get("statusCode")
#                 return "registered" if status_code == 212 else "not registered"
#             else:
#                 return "error"
#     except Exception as e:
#         print(f"TOI API error for mobile {mobile}: {str(e)}")
#         return "error"

# async def check_ajio(session, mobile):
#     try:
#         url = "https://login.web.ajio.com/api/auth/accountCheck"
#         headers = {
#             "Content-Type": "application/json",
#             "Referrer-Policy": "strict-origin-when-cross-origin"
#         }

#         payload = {
#             "mobileNumber": mobile
#         }

#         async with session.post(url, headers=headers, json=payload) as response:
#             print(f"AJIO status code for {mobile}: {response.status}")  # Debug print

#             if response.status == 200:
#                 try:
#                     response_data = await response.json()
#                     print(f"AJIO Response for {mobile}: {response_data}")  # Debug print

#                     is_success = response_data.get("success", False)
#                     return "registered" if is_success else "unregistered"
#                 except Exception as e:
#                     print(f"AJIO JSON parsing error for {mobile}: {str(e)}")
#                     return "error"
#             else:
#                 print(f"AJIO API error response: {await response.text()}")  # Debug print
#                 return "error"

#     except Exception as e:
#         print(f"AJIO API error for mobile {mobile}: {str(e)}")
#         return "error"

# async def check_housing(session, mobile):
#     try:
#         url = "https://mightyzeus-mum.housing.com/api/gql/network-only?apiName=CHECK_LOGIN_DETAIL&emittedFrom=client_buy_SRP&isBot=false&platform=desktop&source=web&source_name=AudienceWeb"
#         headers = {
#             "Accept-Language": "en-US,en;q=0.9,hi;q=0.8,eo;q=0.7",
#             "Origin": "https://housing.com",
#             "Referer": "https://housing.com/in/buy/mumbai/mumbai?paid=true&gad_source=1&gclid=Cj0KCQiA7NO7BhDsARIsADg_hIbpV4Gtz4NgVCMwDgK6m8eg2UsWctD1OLipugNEbgoNa-LDhgagqFcaAv8KEALw_wcB",
#             "app-name": "desktop_web_buyer",
#             "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
#             "sec-ch-ua-mobile": "?0",
#             "phoenix-api-name": "CHECK_LOGIN_DETAIL",
#             "sec-ch-ua-platform": '"Windows"',
#             "sec-fetch-dest": "",
#             "sec-fetch-mode": "cors",
#             "sec-fetch-site": "same-site",
#             "Content-Type": "application/json"
#         }

#         # Remove any country code prefix if present
#         mobile = mobile.lstrip('+').lstrip('91')

#         payload = {
#             "query": "\n  query($email: String, $phone: String) {\n    checkDetail(phone: $phone, email: $email) {\n      key\n      id\n      present\n      status\n      associatedTo\n      message\n    }\n  }\n",
#             "variables": {
#                 "phone": mobile
#             }
#         }

#         async with session.post(url, headers=headers, json=payload) as response:
#             print(f"Housing status code for {mobile}: {response.status}")

#             if response.status == 200:
#                 try:
#                     response_data = await response.json()
#                     print(f"Housing Response for {mobile}: {response_data}")

#                     check_details = response_data.get("data", {}).get("checkDetail", [])
#                     if check_details and len(check_details) > 0:
#                         status = check_details[0].get("status")
#                         return "registered" if status == "verified" else "unregistered"
#                     return "error"
#                 except Exception as e:
#                     print(f"Housing JSON parsing error for {mobile}: {str(e)}")
#                     return "error"
#             else:
#                 print(f"Housing API error response: {await response.text()}")
#                 return "error"
#     except Exception as e:
#         print(f"Housing API error for mobile {mobile}: {str(e)}")
#         return "error"

# async def check_indiamart(session, mobile):
#     try:
#         url = "https://utils.imimg.com/header/js/evaluate.php"
#         headers = {
#             "Accept": "*/*",
#             "Content-Type": "application/x-www-form-urlencoded",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#             "Origin": "https://buyer.indiamart.com",
#             "Referer": "https://buyer.indiamart.com/"
#         }

#         payload = {
#             "username": mobile,
#             "iso": "IN",
#             "modid": "MY",
#             "format": "JSON",
#             "create_user": "0",
#             "originalreferer": "https://buyer.indiamart.com/settings/mysettings/",
#             "GEOIP_COUNTRY_ISO": "IN",
#             "ip": "219.91.135.141",
#             "screen_name": "Sign IN Form Desktop",
#             "Lat_val": "",
#             "Long_val": "",
#             "country": "India",
#             "service_code": "5"
#         }

#         async with session.post(url, headers=headers, data=payload, proxies=proxies) as response:
#             if response.status == 200:
#                 response_text = await response.text()
#                 try:
#                     response_data = json.loads(response_text)


#                     code = response_data.get("code")


#                     if code == "200" or code == 200 :
#                         return "registered"


#                     if code == "204":
#                         return "not registered"


#                     return "error"

#                 except json.JSONDecodeError as e:
#                     print(f"IndiaMART JSON parsing error for mobile {mobile}: {str(e)}")
#                     print(f"Response text: {response_text[:200]}")
#                     return "error"
#             else:
#                 print(f"IndiaMART API error status {response.status} for mobile {mobile}")
#                 return "error"
#     except Exception as e:
#         print(f"IndiaMART API error for mobile {mobile}: {str(e)}")
#         return "error"

# async def process_row(row, session):
#     uid = row["UID"]
#     mobile = str(row["Mobile"]).strip()

#     validation_message, formatted_mobile = validate_and_format_mobile(row)
#     print(validation_message)

#     if formatted_mobile is None:
#         return {"UID": uid, "Indiamart": "invalid", "TimesOfIndia": "invalid"}

#     indiamart_status = await check_indiamart(session, formatted_mobile)
#     toi_status = await check_toi(session, formatted_mobile)
#     housing_status = await check_housing(session, formatted_mobile)
#     ajio_status = await check_ajio(session, formatted_mobile)

#     print(f"UID: {uid}, Mobile: {formatted_mobile}, Indiamart: {indiamart_status}, TimesOfIndia: {toi_status}, Housing: {housing_status}, AJIO: {ajio_status}")
#     return {"UID": uid, "Indiamart": indiamart_status, "TimesOfIndia": toi_status, "Housing": housing_status, "AJIO": ajio_status}

# async def main():
#     input_file = "new.xlsx"
#     output_file = f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

#     start_time = datetime.now()

#     try:
#         data = pd.read_excel(input_file)
#     except Exception as e:
#         print(f"Error reading input file: {e}")
#         return

#     if not {"UID", "Mobile"}.issubset(data.columns):
#         print("Input file must contain 'UID' and 'Mobile' columns.")
#         return

#     timeout = aiohttp.ClientTimeout(total=300)  
#     connector = aiohttp.TCPConnector(limit=10)  

#     async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
#         tasks = [process_row(row, session) for _, row in data.iterrows()]
#         results = await asyncio.gather(*tasks)

#     output_df = pd.DataFrame(results)
#     try:
#         output_df.to_excel(output_file, index=False)
#         print(f"Results saved to {output_file}")
#     except Exception as e:
#         print(f"Error saving output file: {e}")

#     end_time = datetime.now()
#     print(f"Elapsed time: {end_time - start_time}")

# if __name__ == "__main__":
#     asyncio.run(main())

# # import pandas as pd
# # import re
# # import asyncio
# # import aiohttp
# # import json
# # import logging
# # import psutil
# # import time
# # from datetime import datetime
# # from concurrent.futures import ThreadPoolExecutor
# # from pathlib import Path
# # import aiofiles
# # import csv
# # from typing import Dict, Any
# # import queue
# # from threading import Thread

# # def setup_logging():
# #     Path("logs").mkdir(exist_ok=True)
# #     event_logger = logging.getLogger('event_logger')
# #     event_logger.setLevel(logging.INFO)
# #     event_handler = logging.FileHandler(f'logs/events_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
# #     event_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
# #     event_logger.addHandler(event_handler)

# #     perf_logger = logging.getLogger('perf_logger')
# #     perf_logger.setLevel(logging.INFO)
# #     perf_handler = logging.FileHandler(f'logs/performance_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
# #     perf_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
# #     perf_logger.addHandler(perf_handler)

# #     return event_logger, perf_logger

# # class PerformanceMonitor(Thread):
# #     def __init__(self, interval: float, perf_logger: logging.Logger):
# #         super().__init__()
# #         self.interval = interval
# #         self.perf_logger = perf_logger
# #         self.running = True

# #     def run(self):
# #         while self.running:
# #             cpu_percent = psutil.cpu_percent(interval=1)
# #             memory = psutil.virtual_memory()
# #             self.perf_logger.info(
# #                 f"CPU Usage: {cpu_percent}% | Memory Usage: {memory.percent}% | Available Memory: {memory.available / 1024 / 1024:.2f} MB"
# #             )
# #             time.sleep(self.interval)

# #     def stop(self):
# #         self.running = False

# # class ResultWriter(Thread):
# #     def __init__(self, output_file: str):
# #         super().__init__()
# #         self.output_file = output_file
# #         self.queue = queue.Queue()
# #         self.running = True

# #         headers = ["UID", "Mobile", "Indiamart", "TimesOfIndia", "Housing", "AJIO", "Timestamp"]
# #         with open(self.output_file, 'w', newline='') as f:
# #             writer = csv.writer(f)
# #             writer.writerow(headers)

# #     def add_result(self, result: Dict[str, Any]):
# #         self.queue.put(result)

# #     def run(self):
# #         while self.running or not self.queue.empty():
# #             try:
# #                 result = self.queue.get(timeout=1)
# #                 with open(self.output_file, 'a', newline='') as f:
# #                     writer = csv.writer(f)
# #                     writer.writerow([
# #                         result["UID"],
# #                         result.get("Mobile", ""),
# #                         result["Indiamart"],
# #                         result["TimesOfIndia"],
# #                         result["Housing"],
# #                         result["AJIO"],
# #                         datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# #                     ])
# #             except queue.Empty:
# #                 continue

# #     def stop(self):
# #         self.running = False

# # async def check_toi(session: aiohttp.ClientSession, mobile: str, event_logger: logging.Logger) -> str:
# #     start_time = time.time()
# #     event_logger.info(f"Starting TOI check for {mobile}")

# #     try:
# #         url = "https://jsso.indiatimes.com/sso/crossapp/identity/web/checkUserExists"
# #         headers = {
# #             "Content-Type": "application/json",
# #             "Accept": "*/*",
# #             "Referer": "https://timesofindia.indiatimes.com/",
# #             "Origin": "https://timesofindia.indiatimes.com",
# #             "channel": "toi",
# #             "sdkversion": "0.7.993"
# #         }
# #         payload = {"identifier": mobile}

# #         async with session.post(url, headers=headers, json=payload) as response:
# #             response_time = time.time() - start_time
# #             event_logger.info(f"TOI API response time for {mobile}: {response_time:.2f}s")

# #             if response.status == 200:
# #                 response_data = await response.json()
# #                 status_code = response_data.get("data", {}).get("statusCode")
# #                 result = "registered" if status_code == 212 else "not registered"
# #                 event_logger.info(f"TOI check result for {mobile}: {result}")
# #                 return result
# #             else:
# #                 event_logger.error(f"TOI API error status {response.status} for {mobile}")
# #                 return "error"
# #     except Exception as e:
# #         event_logger.error(f"TOI API error for {mobile}: {str(e)}")
# #         return "error"

# # async def check_ajio(session: aiohttp.ClientSession, mobile: str, event_logger: logging.Logger) -> str:
# #     start_time = time.time()
# #     event_logger.info(f"Starting AJIO check for {mobile}")

# #     try:
# #         url = "https://login.web.ajio.com/api/auth/accountCheck"
# #         headers = {
# #             "Content-Type": "application/json",
# #             "Referrer-Policy": "strict-origin-when-cross-origin"
# #         }
# #         payload = {"mobileNumber": mobile}

# #         async with session.post(url, headers=headers, json=payload) as response:
# #             response_time = time.time() - start_time
# #             event_logger.info(f"AJIO API response time for {mobile}: {response_time:.2f}s")

# #             if response.status == 200:
# #                 response_data = await response.json()
# #                 is_success = response_data.get("success", False)
# #                 result = "registered" if is_success else "unregistered"
# #                 event_logger.info(f"AJIO check result for {mobile}: {result}")
# #                 return result
# #             else:
# #                 event_logger.error(f"AJIO API error status {response.status} for {mobile}")
# #                 return "error"
# #     except Exception as e:
# #         event_logger.error(f"AJIO API error for {mobile}: {str(e)}")
# #         return "error"

# # async def check_housing(session: aiohttp.ClientSession, mobile: str, event_logger: logging.Logger) -> str:
# #     start_time = time.time()
# #     event_logger.info(f"Starting Housing check for {mobile}")

# #     try:
# #         url = "https://mightyzeus-mum.housing.com/api/gql/network-only?apiName=CHECK_LOGIN_DETAIL&emittedFrom=client_buy_SRP&isBot=false&platform=desktop&source=web&source_name=AudienceWeb"
# #         headers = {
# #             "Accept-Language": "en-US,en;q=0.9,hi;q=0.8,eo;q=0.7",
# #             "Origin": "https://housing.com",
# #             "Referer": "https://housing.com/in/buy/mumbai/mumbai?paid=true&gad_source=1&gclid=Cj0KCQiA7NO7BhDsARIsADg_hIbpV4Gtz4NgVCMwDgK6m8eg2UsWctD1OLipugNEbgoNa-LDhgagqFcaAv8KEALw_wcB",
# #             "app-name": "desktop_web_buyer",
# #             "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
# #             "sec-ch-ua-mobile": "?0",
# #             "phoenix-api-name": "CHECK_LOGIN_DETAIL",
# #             "sec-ch-ua-platform": '"Windows"',
# #             "sec-fetch-dest": "",
# #             "sec-fetch-mode": "cors",
# #             "sec-fetch-site": "same-site",
# #             "Content-Type": "application/json"
# #         }

# #         mobile = mobile.lstrip('+').lstrip('91')
# #         payload = {
# #             "query": "\n  query($email: String, $phone: String) {\n    checkDetail(phone: $phone, email: $email) {\n      key\n      id\n      present\n      status\n      associatedTo\n      message\n    }\n  }\n",
# #             "variables": {"phone": mobile}
# #         }

# #         async with session.post(url, headers=headers, json=payload) as response:
# #             response_time = time.time() - start_time
# #             event_logger.info(f"Housing API response time for {mobile}: {response_time:.2f}s")

# #             if response.status == 200:
# #                 response_data = await response.json()
# #                 check_details = response_data.get("data", {}).get("checkDetail", [])
# #                 if check_details and len(check_details) > 0:
# #                     status = check_details[0].get("status")
# #                     result = "registered" if status == "verified" else "unregistered"
# #                     event_logger.info(f"Housing check result for {mobile}: {result}")
# #                     return result
# #                 return "error"
# #             else:
# #                 event_logger.error(f"Housing API error status {response.status} for {mobile}")
# #                 return "error"
# #     except Exception as e:
# #         event_logger.error(f"Housing API error for {mobile}: {str(e)}")
# #         return "error"

# # async def check_indiamart(session: aiohttp.ClientSession, mobile: str, event_logger: logging.Logger) -> str:
# #     start_time = time.time()
# #     event_logger.info(f"Starting IndiaMART check for {mobile}")

# #     try:
# #         url = "https://utils.imimg.com/header/js/evaluate.php"
# #         headers = {
# #             "Accept": "*/*",
# #             "Content-Type": "application/x-www-form-urlencoded",
# #             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
# #             "Origin": "https://buyer.indiamart.com",
# #             "Referer": "https://buyer.indiamart.com/"
# #         }

# #         payload = {
# #             "username": mobile,
# #             "iso": "IN",
# #             "modid": "MY",
# #             "format": "JSON",
# #             "create_user": "0",
# #             "originalreferer": "https://buyer.indiamart.com/settings/mysettings/",
# #             "GEOIP_COUNTRY_ISO": "IN",
# #             "ip": "219.91.135.141",
# #             "screen_name": "Sign IN Form Desktop",
# #             "Lat_val": "",
# #             "Long_val": "",
# #             "country": "India",
# #             "service_code": "5"
# #         }

# #         async with session.post(url, headers=headers, data=payload) as response:
# #             response_time = time.time() - start_time
# #             event_logger.info(f"IndiaMART API response time for {mobile}: {response_time:.2f}s")

# #             if response.status == 200:
# #                 response_text = await response.text()
# #                 try:
# #                     response_data = json.loads(response_text)
# #                     code = response_data.get("code")
# #                     if code in ["200", 200]:
# #                         result = "registered"
# #                     elif code == "204":
# #                         result = "not registered"
# #                     else:
# #                         result = "error"
# #                     event_logger.info(f"IndiaMART check result for {mobile}: {result}")
# #                     return result
# #                 except json.JSONDecodeError as e:
# #                     event_logger.error(f"IndiaMART JSON parsing error for {mobile}: {str(e)}")
# #                     return "error"
# #             else:
# #                 event_logger.error(f"IndiaMART API error status {response.status} for {mobile}")
# #                 return "error"
# #     except Exception as e:
# #         event_logger.error(f"IndiaMART API error for {mobile}: {str(e)}")
# #         return "error"

# # def validate_and_format_mobile(row):
# #     uid, mobile = row['UID'], str(row['Mobile'])

# #     if pd.isna(mobile) or mobile.strip() == "":
# #         return f"Invalid mobile number format for UID {uid}: {mobile}", None

# #     mobile = re.sub(r'\D', '', mobile)

# #     if len(mobile) == 10:
# #         mobile = "91" + mobile
# #     elif len(mobile) == 12 and mobile.startswith("91"):
# #         pass
# #     else:
# #         return f"Invalid mobile number format for UID {uid}: {mobile}", None

# #     return f"Valid mobile number for UID {uid}: {mobile}", mobile

# # async def process_batch(batch: pd.DataFrame, session: aiohttp.ClientSession, 
# #                        event_logger: logging.Logger, result_writer: ResultWriter) -> None:
# #     async def process_single_row(row):
# #         uid = row["UID"]
# #         mobile = str(row["Mobile"]).strip()

# #         validation_message, formatted_mobile = validate_and_format_mobile(row)
# #         event_logger.info(validation_message)

# #         if formatted_mobile is None:
# #             result = {
# #                 "UID": uid,
# #                 "Mobile": mobile,
# #                 "Indiamart": "invalid",
# #                 "TimesOfIndia": "invalid",
# #                 "Housing": "invalid",
# #                 "AJIO": "invalid"
# #             }
# #         else:
# #             results = await asyncio.gather(
# #                 check_indiamart(session, formatted_mobile, event_logger),
# #                 check_toi(session, formatted_mobile, event_logger),
# #                 check_housing(session, formatted_mobile, event_logger),
# #                 check_ajio(session, formatted_mobile, event_logger)
# #             )

# #             result = {
# #                 "UID": uid,
# #                 "Mobile": formatted_mobile,
# #                 "Indiamart": results[0],
# #                 "TimesOfIndia": results[1],
# #                 "Housing": results[2],
# #                 "AJIO": results[3]
# #             }

# #         result_writer.add_result(result)
# #         event_logger.info(f"Processed UID: {uid}, Mobile: {formatted_mobile}")

# #     await asyncio.gather(*(process_single_row(row) for _, row in batch.iterrows()))

# # async def main():
# #     event_logger, perf_logger = setup_logging()
# #     perf_monitor = PerformanceMonitor(interval=5, perf_logger=perf_logger)
# #     perf_monitor.start()

# #     output_file = f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
# #     result_writer = ResultWriter(output_file)
# #     result_writer.start()

# #     start_time = datetime.now()
# #     event_logger.info("Starting process")

# #     try:
# #         input_file = "new.xlsx"
# #         data = pd.read_excel(input_file)
# #         event_logger.info(f"Read {len(data)} rows from input file")

# #         timeout = aiohttp.ClientTimeout(total=300)
# #         connector = aiohttp.TCPConnector(limit=50)

# #         batch_size = 50
# #         batches = [data[i:i + batch_size] for i in range(0, len(data), batch_size)]

# #         async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
# #             for batch_num, batch in enumerate(batches, 1):
# #                 event_logger.info(f"Processing batch {batch_num}/{len(batches)}")
# #                 await process_batch(batch, session, event_logger, result_writer)

# #     except Exception as e:
# #         event_logger.error(f"Error in main process: {str(e)}")
# #     finally:
# #         perf_monitor.stop()
# #         perf_monitor.join()

# #         result_writer.stop()
# #         result_writer.join()

# #         end_time = datetime.now()
# #         elapsed_time = end_time - start_time
# #         event_logger.info(f"Process completed. Total time: {elapsed_time}")
# #         print(f"Process completed. Results saved to {output_file}")
# #         print(f"Logs saved in the 'logs' directory")

# # if __name__ == "__main__":
# #     asyncio.run(main())


import re
import asyncio
import aiohttp
import json
import redis
from datetime import datetime

# Initialize Redis client
redis_client = redis.Redis(
    host='redis-19800.crce179.ap-south-1-1.ec2.redns.redis-cloud.com',
    port=19800,
    decode_responses=True,
    username="default",
    password="JMPog04EGI2MVcbO3HDPC9clDNyztfBX",
)

proxies = {
    "http": "geonode_1VvZ28sUKX:3860618c-044d-4622-af4e-95200f09ce05@92.204.164.15:9000",
    "https": "geonode_1VvZ28sUKX:3860618c-044d-4622-af4e-95200f09ce05@92.204.164.15:9000",
}


def validate_and_format_mobile(uid, mobile):
    if not mobile or mobile.strip() == "":
        return f"Invalid mobile number format for UID {uid}: {mobile}", None

    mobile = re.sub(r'\D', '', mobile)

    if len(mobile) == 10:
        mobile = "91" + mobile
    elif len(mobile) == 12 and mobile.startswith("91"):
        pass
    else:
        return f"Invalid mobile number format for UID {uid}: {mobile}", None

    return f"Valid mobile number for UID {uid}: {mobile}", mobile


async def check_toi(session, mobile):
    try:
        url = "https://jsso.indiatimes.com/sso/crossapp/identity/web/checkUserExists"
        headers = {
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Referer": "https://timesofindia.indiatimes.com/",
            "Origin": "https://timesofindia.indiatimes.com",
            "channel": "toi",
            "sdkversion": "0.7.993"
        }
        payload = {"identifier": mobile}
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                response_data = await response.json()
                status_code = response_data.get("data", {}).get("statusCode")
                return "registered" if status_code == 212 else "not registered"
            else:
                return "error"
    except Exception as e:
        print(f"TOI API error for mobile {mobile}: {str(e)}")
        return "error"


async def check_ajio(session, mobile):
    try:
        url = "https://login.web.ajio.com/api/auth/accountCheck"
        headers = {
            "Content-Type": "application/json",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }

        payload = {
            "mobileNumber": mobile
        }

        async with session.post(url, headers=headers, json=payload) as response:
            print(f"AJIO status code for {mobile}: {response.status}")  # Debug print

            if response.status == 200:
                try:
                    response_data = await response.json()
                    print(f"AJIO Response for {mobile}: {response_data}")  # Debug print

                    is_success = response_data.get("success", False)
                    return "registered" if is_success else "unregistered"
                except Exception as e:
                    print(f"AJIO JSON parsing error for {mobile}: {str(e)}")
                    return "error"
            else:
                print(f"AJIO API error response: {await response.text()}")  # Debug print
                return "error"

    except Exception as e:
        print(f"AJIO API error for mobile {mobile}: {str(e)}")
        return "error"


async def check_housing(session, mobile):
    try:
        url = "https://mightyzeus-mum.housing.com/api/gql/network-only?apiName=CHECK_LOGIN_DETAIL&emittedFrom=client_buy_SRP&isBot=false&platform=desktop&source=web&source_name=AudienceWeb"
        headers = {
            "Accept-Language": "en-US,en;q=0.9,hi;q=0.8,eo;q=0.7",
            "Origin": "https://housing.com",
            "Referer": "https://housing.com/in/buy/mumbai/mumbai?paid=true&gad_source=1&gclid=Cj0KCQiA7NO7BhDsARIsADg_hIbpV4Gtz4NgVCMwDgK6m8eg2UsWctD1OLipugNEbgoNa-LDhgagqFcaAv8KEALw_wcB",
            "app-name": "desktop_web_buyer",
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "phoenix-api-name": "CHECK_LOGIN_DETAIL",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "Content-Type": "application/json"
        }

        # Remove any country code prefix if present
        mobile = mobile.lstrip('+').lstrip('91')

        payload = {
            "query": "\n  query($email: String, $phone: String) {\n    checkDetail(phone: $phone, email: $email) {\n      key\n      id\n      present\n      status\n      associatedTo\n      message\n    }\n  }\n",
            "variables": {
                "phone": mobile
            }
        }

        async with session.post(url, headers=headers, json=payload) as response:
            print(f"Housing status code for {mobile}: {response.status}")

            if response.status == 200:
                try:
                    response_data = await response.json()
                    print(f"Housing Response for {mobile}: {response_data}")

                    check_details = response_data.get("data", {}).get("checkDetail", [])
                    if check_details and len(check_details) > 0:
                        status = check_details[0].get("status")
                        return "registered" if status == "verified" else "unregistered"
                    return "error"
                except Exception as e:
                    print(f"Housing JSON parsing error for {mobile}: {str(e)}")
                    return "error"
            else:
                print(f"Housing API error response: {await response.text()}")
                return "error"
    except Exception as e:
        print(f"Housing API error for mobile {mobile}: {str(e)}")
        return "error"


async def check_indiamart(session, mobile):
    try:
        url = "https://utils.imimg.com/header/js/evaluate.php"
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Origin": "https://buyer.indiamart.com",
            "Referer": "https://buyer.indiamart.com/"
        }

        payload = {
            "username": mobile,
            "iso": "IN",
            "modid": "MY",
            "format": "JSON",
            "create_user": "0",
            "originalreferer": "https://buyer.indiamart.com/settings/mysettings/",
            "GEOIP_COUNTRY_ISO": "IN",
            "ip": "219.91.135.141",
            "screen_name": "Sign IN Form Desktop",
            "Lat_val": "",
            "Long_val": "",
            "country": "India",
            "service_code": "5"
        }

        async with session.post(url, headers=headers, data=payload, proxies=proxies) as response:
            if response.status == 200:
                response_text = await response.text()
                try:
                    response_data = json.loads(response_text)

                    code = response_data.get("code")

                    if code == "200" or code == 200:
                        return "registered"

                    if code == "204":
                        return "not registered"

                    return "error"

                except json.JSONDecodeError as e:
                    print(f"IndiaMART JSON parsing error for mobile {mobile}: {str(e)}")
                    print(f"Response text: {response_text[:200]}")
                    return "error"
            else:
                print(f"IndiaMART API error status {response.status} for mobile {mobile}")
                return "error"
    except Exception as e:
        print(f"IndiaMART API error for mobile {mobile}: {str(e)}")
        return "error"


async def process_row(data, session):
    mobile = data
    uid = "NA"

    validation_message, formatted_mobile = validate_and_format_mobile(uid, mobile)
    print(validation_message)

    if formatted_mobile is None:
        await redis_client.lpush("invalid_data", json.dumps({"UID": uid, "Mobile": mobile, "Status": "Invalid"}))
        return

    indiamart_status = await check_indiamart(session, formatted_mobile)
    toi_status = await check_toi(session, formatted_mobile)
    housing_status = await check_housing(session, formatted_mobile)
    ajio_status = await check_ajio(session, formatted_mobile)

    print(
        f"UID: {uid}, Mobile: {formatted_mobile}, Indiamart: {indiamart_status}, TimesOfIndia: {toi_status}, Housing: {housing_status}, AJIO: {ajio_status}")

    # Push results to Redis lists
    redis_client.lpush("indiamart_results",
                       json.dumps({"UID": uid, "Mobile": formatted_mobile, "Status": indiamart_status}))
    redis_client.lpush("toi_results", json.dumps({"UID": uid, "Mobile": formatted_mobile, "Status": toi_status}))
    redis_client.lpush("housing_results",
                       json.dumps({"UID": uid, "Mobile": formatted_mobile, "Status": housing_status}))
    redis_client.lpush("ajio_results",
                       json.dumps({"UID": uid, "Mobile": formatted_mobile, "Status": ajio_status}))


async def main():
    timeout = aiohttp.ClientTimeout(total=300)
    connector = aiohttp.TCPConnector(limit=10)

    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        while True:
            # Fetch data from Redis list `mobile_data`
            data_json = redis_client.brpop("india_ajio_housing_toi_mobile_data", timeout=30)  # Wait for data
            if not data_json:
                print("No more data to process. Exiting.")
                break

            try:
                data = json.loads(data_json[1])  # Parse JSON
                await process_row(str(data), session)
            except Exception as e:
                print(f"Error processing data: {e}")


if __name__ == "__main__":
    asyncio.run(main())
