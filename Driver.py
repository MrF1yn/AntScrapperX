import csv
from urllib.parse import urlparse
import psycopg2
import redis
import threading
import time

# Redis connection setup
redis_client = redis.Redis(
    host='redis-19800.crce179.ap-south-1-1.ec2.redns.redis-cloud.com',
    port=19800,
    decode_responses=True,
    username="default",
    password="JMPog04EGI2MVcbO3HDPC9clDNyztfBX",
)

# db_url = "postgresql://postgres:qS1hAyZFcQFqrre6@db.lthjdpnfcewonemuleed.supabase.co:5432/postgres"
# db_url = "postgresql://postgres.lthjdpnfcewonemuleed:qS1hAyZFcQFqrre6@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
db_url = "postgresql://postgres.ufgcfatyimxxhsnrmtzf:W0j4re9WW8kEtUbm@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

# Parse the database URL

pg_conn = psycopg2.connect(db_url)
pg_cursor = pg_conn.cursor()

# Redis list names
redis_lists_numbers = ['amazon', 'flipkart', 'whatsapp', "india_ajio_housing_toi_mobile_data", "microsoft_number"]
redis_lists_emails = ['quora',  "microsoft_email"]
redis_lists_numbers_extras = ["indiamart", "housing", "toi", "ajio"]
redis_results_channels = [f"{channel}_results" for channel in
                          redis_lists_numbers + redis_lists_emails + redis_lists_numbers_extras]

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
                if i >= 100:
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
    Continuously checks Redis lists for new results and updates them to PostgreSQL when buffer size reaches 50 or after a timeout.
    """
    global results_buffer
    last_flush_time = time.time()
    flush_timeout = 30  # Timeout in seconds

    while True:
        for channel in redis_results_channels:
            try:
                result = redis_client.rpop(channel)
                if result:
                    # Parse the Redis result (assuming key=value format)
                    scrapper_id, email, status, timestamp = result.split(',')
                    print(f"Received result for {email}: {status} from {channel}")
                    last_flush_time = time.time()
                    # Add to buffer
                    with buffer_lock:
                        results_buffer.append((email, status + "," + channel))

                    # If buffer reaches 50, insert into PostgreSQL
                    if len(results_buffer) >= 50:
                        flush_to_postgresql()

            except Exception as e:
                print(f"Error processing Redis channel {channel}: {e}")

        # Check if the timeout has been reached
        if time.time() - last_flush_time >= flush_timeout:
            flush_to_postgresql()
            last_flush_time = time.time()

        # time.sleep(1)  # Avoid tight loop


def flush_to_postgresql():
    """
    Flushes the results buffer to the PostgreSQL table, updating or inserting records as needed.
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
                channel = channel.replace("_results", "")
                date = time.strftime('%Y-%m-%d %H:%M:%S')

                # Check if the number exists in the table
                pg_cursor.execute("SELECT * FROM results WHERE numbers = %s", (key,))
                existing_record = pg_cursor.fetchone()

                if existing_record:
                    # Update the existing record
                    update_query = f"UPDATE results SET {channel} = %s, {channel}_date = %s WHERE numbers = %s"
                    pg_cursor.execute(update_query, (status, date, key))
                    print(f"Updated {key} for channel {channel}")
                else:
                    # Insert a new record
                    insert_query = "INSERT INTO results (numbers, {channel}, {channel}_date) VALUES (%s, %s, %s)"
                    formatted_query = insert_query.format(channel=channel)
                    pg_cursor.execute(formatted_query, (key, status, date))
                    print(f"Inserted new record for {key} with channel {channel}")

            # Commit the changes
            pg_conn.commit()
            print(f"Processed {len(results_buffer)} rows.")

            # Clear the buffer
            results_buffer = []

        except psycopg2.Error as e:
            print(f"PostgreSQL error: {e}")


if __name__ == "__main__":
    # Start the Redis monitoring thread
    redis_thread = threading.Thread(target=process_redis_results, daemon=True)
    redis_thread.start()

    # Example usage
    # push_to_redis("phone-numbers-csv.csv", redis_lists_numbers)
    # push_to_redis("emails-csv.csv", redis_lists_emails)

    # Keep the main thread alive
    while True:
        time.sleep(1)
