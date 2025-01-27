import random
import redis
import csv
import time

import requests

url = "https://www.quora.com/graphql/gql_para_POST?q=SignupEmailForm_validateEmail_Query"
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

# Prepare to write to CSV
with open('quora_results.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Email", "Status"])  # CSV Header

    # Fetch phone numbers from Redis list using BRPOP
    while True:
        # Block and wait for a phone number from the Redis list 'flipkart_phone_list'
        email = redis_client.brpop('quora', timeout=30)  # timeout=0 means it blocks indefinitely
        if not email:
            print("No more emails to process. Exiting.")
            break
        if email:
            email = email[1]  # Extracting the phone number and converting bytes to string

            try:
                headers = {
                    "accept": "/",
                    "accept-language": "en-US,en;q=0.9,hi;q=0.8,eo;q=0.7",
                    "content-type": "application/json",
                    "cookie": "m-login=0; m-b=1YpQ4RkBLweUVfNKAiYnqQ==; m-b_lax=1YpQ4RkBLweUVfNKAiYnqQ==; m-b_strict=1YpQ4RkBLweUVfNKAiYnqQ==; m-s=2EGyzFLMP-wzB0G-FDcX7w==; m-uid=None; m-dynamicFontSize=regular; m-themeStrategy=auto; m-theme=dark; __gads=ID=2292c8c174b842cf:T=1736770213:RT=1736770213:S=ALNI_MZitGF2Z0Ku_niBSF5QDMCULrrTZQ; __gpi=UID=00000fe82295c249:T=1736770213:RT=1736770213:S=ALNI_MaI-S0UfbsIQRXjW7i6oL4V437xAA; __eoi=ID=739ed727f9f9fa87:T=1736770213:RT=1736770213:S=AA-AfjaWSl2MjB_f86xeVgEOh743; m-sa=1; m-signup_form_type=dismissible_wall; m-login_redirect_url=https%3A%2F%2Fquorablog.quora.com%2F",
                    "dnt": "1",
                    "origin": "https://www.quora.com",
                    "priority": "u=1, i",
                    "quora-broadcast-id": "main-w-chan118-8888-react_ivugjxdmchbknypz-ojRi",
                    "quora-canary-revision": "false",
                    "quora-formkey": "a1c4f22fe0bdda9cca885ad4dda5f175",
                    "quora-page-creation-time": "1736949387840231",
                    "quora-revision": "f7cc16306f4ac4132a8f8558d9727fe171f3aaa3",
                    "quora-window-id": "react_ivugjxdmchbknypz",
                    "referer": "https://www.quora.com/",
                    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": "\"Windows\"",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
                }

                payload = {
                    "queryName": "SignupEmailForm_validateEmail_Query",
                    "variables": {
                        "email": email
                    },
                    "extensions": {
                        "hash": "1db80096407be846d5581fe1b42b12fd05e0b40a5d3095ed40a0b4bd28f49fe7"
                    }
                }

                response = requests.post(url, headers=headers, json=payload, proxies=proxies)
                # response = requests.post(url, headers=headers, json=payload)
                status = response.json()["data"]["validateEmail"]
                print("response", response.json())
                status = "Present" if status == "IN_USE" else "Absent"
                print(email, status)
                writer.writerow([email, status])
                redis_client.lpush("quora_results", f"{email},{status}")
            except Exception as e:
                print(f"Error processing number {email}: {str(e)}")
                redis_client.lpush("quora_results", f"{email},Error")
                writer.writerow([email, "Error"])
    file.flush()
