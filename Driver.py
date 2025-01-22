import csv
from urllib.parse import urlparse

import redis
import threading
import time
import mysql.connector

# Redis connection setup
redis_client = redis.Redis(
    host='redis-19800.crce179.ap-south-1-1.ec2.redns.redis-cloud.com',
    port=19800,
    decode_responses=True,
    username="default",
    password="JMPog04EGI2MVcbO3HDPC9clDNyztfBX",
)

DATABASE_URL = "postgresql://postgres:qS1hAyZFcQFqrre6@db.lthjdpnfcewonemuleed.supabase.co:5432/postgrese"

# Parse the database URL
db_url = urlparse(DATABASE_URL)
mysql_conn = mysql.connector.connect(
    host=db_url.hostname,
    port=db_url.port,
    user=db_url.username,
    password=db_url.password,
    database=db_url.path.lstrip('/'),
)
mysql_cursor = mysql_conn.cursor()

# Redis list names
redis_lists_numbers = ['amazon', 'flipkart', 'ajio', 'whatsapp']
redis_lists_emails = ['quora']
redis_results_channels = [f"{channel}_results" for channel in redis_lists_numbers + redis_lists_emails]

# Array to store results before MySQL insertion
results_buffer = []

# Lock for thread safety
buffer_lock = threading.Lock()

def format_phone_number(phone_number):
    """
    Format phone number according to the rules:
    - If length > 10, remove first two digits

    Args:
        phone_number (str): The phone number to format

    Returns:
        str: Formatted phone number
    """
    if "@" in phone_number:
        return phone_number
    if len(phone_number) > 10:
        return phone_number[2:]
    return phone_number

def push_to_redis(file_path, redis_lists):
    """
    Reads a CSV file containing phone numbers and pushes each number to all Redis lists.

    Args:
        file_path (str): Path to the CSV file.
    """
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader, None)  # Skip header row if it exists

            # Process each phone number
            for i, row in enumerate(csv_reader):
                if i >= 1000:
                    break
                if row:
                    phone_number = row[0]
                    formatted_number = format_phone_number(phone_number)

                    # Push the formatted phone number to all Redis lists
                    for list_name in redis_lists:
                        redis_client.lpush(list_name, formatted_number)
                        print(f"Pushed {formatted_number} into {list_name} (original: {phone_number})")

    except FileNotFoundError:
        print("Error: The specified file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_redis_results():
    """
    Continuously checks Redis lists for new results and updates them to MySQL when buffer size reaches 50.
    """
    global results_buffer

    while True:
        for channel in redis_results_channels:
            try:
                result = redis_client.rpop(channel)
                if result:
                    # Parse the Redis result (assuming key=value format)
                    key, value = result.split(',', 1)

                    # Add to buffer
                    with buffer_lock:
                        results_buffer.append((key, value+","+channel))

                    # If buffer reaches 50, insert into MySQL
                    if len(results_buffer) >= 50:
                        flush_to_mysql()

            except Exception as e:
                print(f"Error processing Redis channel {channel}: {e}")

        time.sleep(1)  # Avoid tight loop

def flush_to_mysql():
    """
    Flushes the results buffer to the MySQL table, updating or inserting records as needed.
    """
    global results_buffer

    with buffer_lock:
        if not results_buffer:
            return

        try:
            for key, value in results_buffer:
                # Parse the value to determine the channel and date
                parts = value.split(',')
                if len(parts) != 2:
                    print(f"Skipping invalid data format: {value}")
                    continue

                status, channel = parts
                date = time.strftime('%Y-%m-%d %H:%M:%S')

                # Check if the number exists in the table
                mysql_cursor.execute("SELECT * FROM results WHERE numbers = %s", (key,))
                existing_record = mysql_cursor.fetchone()

                if existing_record:
                    # Update the existing record
                    update_query = f"UPDATE results SET {channel} = %s, {channel}_date = %s WHERE numbers = %s"
                    mysql_cursor.execute(update_query, (status, date, key))
                    print(f"Updated {key} for channel {channel}")
                else:
                    # Insert a new record
                    insert_query = "INSERT INTO results (numbers, {channel}, {channel}_date) VALUES (%s, %s, %s)"
                    formatted_query = insert_query.format(channel)
                    mysql_cursor.execute(formatted_query, (key, status, date))
                    print(f"Inserted new record for {key} with channel {channel}")

            # Commit the changes
            mysql_conn.commit()
            print(f"Processed {len(results_buffer)} rows.")

            # Clear the buffer
            results_buffer = []

        except mysql.connector.Error as e:
            print(f"MySQL error: {e}")
if __name__ == "__main__":
    # Start the Redis monitoring thread
    # redis_thread = threading.Thread(target=process_redis_results, daemon=True)
    # redis_thread.start()

    # Example usage
    push_to_redis("phone-numbers-csv.csv", redis_lists_numbers)
    push_to_redis("emails-csv.csv", redis_lists_emails)

    # Keep the main thread alive
    while True:
        time.sleep(1)
