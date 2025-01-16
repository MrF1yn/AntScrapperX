import requests

# Define the URLs
login_url = "https://erp.happyecom.com/index/user_login"
report_url = "https://erp.happyecom.com/order_payment_reportnewlogic/DownloadBrandExcelReport"

# Login credentials as a single form data key-value pair
login_data = {
    "data": "email=accounts%40jumbodistributors.in&password=12345"
}

# Report request data
report_data_mtd = {
    "select-date": "01-Jan-2025 - 15-Jan-2025",
    "select-date-return": "",
    "select-date-payment": "",
    "channel_Type": "9eg7tamixr8798mj-Flipkart Internet Private Limited"
}
report_data_ytd = {
    "select-date": "01-Jan-2024 - 15-Jan-2025",
    "select-date-return": "",
    "select-date-payment": "",
    "channel_Type": "9eg7tamixr8798mj-Flipkart Internet Private Limited"
}

# Create a session
session = requests.Session()

try:
    # Step 1: Log in
    login_response = session.post(login_url, data=login_data)

    # Check if login was successful
    if login_response.status_code == 200 and "success" in login_response.text.lower():
        print("Login successful!")
    else:
        print("Login failed!")
        print("Response:", login_response.text)
        exit()

    # Step 2: Request the Excel report
    # headers = {"Content-Type": "application/x-www-form-urlencoded"}
    report_response = session.post(report_url, data=report_data_mtd)

    # Check if the response is successful
    if report_response.status_code == 200:
        # Save the Excel file
        with open("Flipkart_Brand_report_MTD.xlsx", "wb") as file:
            file.write(report_response.content)
        print("MTD Report downloaded successfully as 'Flipkart_Brand_report_MTD.xlsx'.")
    else:
        print("Failed to download the report.")
        print("Status Code:", report_response.status_code)
        print("Response:", report_response.text)

    report_response = session.post(report_url, data=report_data_ytd)
    # Check if the response is successful
    if report_response.status_code == 200:
        # Save the Excel file
        with open("Flipkart_Brand_report_YTD.xlsx", "wb") as file:
            file.write(report_response.content)
        print("YTD Report downloaded successfully as 'Flipkart_Brand_report_YTD.xlsx'.")
    else:
        print("Failed to download the report.")
        print("Status Code:", report_response.status_code)
        print("Response:", report_response.text)

except Exception as e:
    print("An error occurred:", str(e))
