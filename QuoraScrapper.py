import random
import redis
import csv
import time
import aiohttp
import asyncio

scrapper_id = random.randint(100000, 999999)
start_time = int(time.time() * 1000)
url = "https://www.quora.com/graphql/gql_para_POST?q=SignupEmailForm_validateEmail_Query"
redis_client = redis.Redis(
    host='redis-19800.crce179.ap-south-1-1.ec2.redns.redis-cloud.com',
    port=19800,
    decode_responses=True,
    username="default",
    password="JMPog04EGI2MVcbO3HDPC9clDNyztfBX",
)

proxies = {
    "http": f"geonode_1VvZ28sUKX:3860618c-044d-4622-af4e-95200f09ce05@premium-residential.geonode.com:{random.randint(9000, 9010)}",
    "https": f"geonode_1VvZ28sUKX:3860618c-044d-4622-af4e-95200f09ce05@premium-residential.geonode.com:{random.randint(9000, 9010)}",
}

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
USERNAME = 'geonode_1VvZ28sUKX'
PASSWORD = '3860618c-044d-4622-af4e-95200f09ce05'
async def fetch_email_status(session, email):
    payload = {
        "queryName": "SignupEmailForm_validateEmail_Query",
        "variables": {
            "email": email
        },
        "extensions": {
            "hash": "1db80096407be846d5581fe1b42b12fd05e0b40a5d3095ed40a0b4bd28f49fe7"
        }
    }
    async with session.post(url, headers=headers, json=payload,proxy="http://premium-residential.geonode.com:9000",
                                proxy_auth=aiohttp.BasicAuth(USERNAME, PASSWORD)) as response:
        return await response.json()

async def process_emails():
    async with aiohttp.ClientSession() as session:
        with open('quora_results.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Email", "Status"])  # CSV Header

            while True:
                email = redis_client.brpop('quora', timeout=30)
                if not email:
                    print("No more emails to process. Exiting.")
                    end_time = int(time.time() * 1000)
                    print(f"Runtime: {end_time - start_time}ms")
                    break
                if email:
                    email = email[1]
                    try:
                        response = await fetch_email_status(session, email)
                        status = response["data"]["validateEmail"]
                        status = "Present" if status == "IN_USE" else "Absent"
                        print(email, status)
                        writer.writerow([email, status])
                        redis_client.lpush("quora_results", f"{scrapper_id},{email},{status},{int(time.time() * 1000)}")
                    except Exception as e:
                        print(f"Error processing number {email}: {str(e)}")
                        redis_client.lpush("quora_results", f"{scrapper_id},{email},Error,{int(time.time() * 1000)}")
                        writer.writerow([email, "Error"])
            file.flush()

if __name__ == "__main__":
    asyncio.run(process_emails())