import csv
import redis

# Redis connection setup
redis_client = redis.Redis(
    host='redis-19800.crce179.ap-south-1-1.ec2.redns.redis-cloud.com',
    port=19800,
    decode_responses=True,
    username="default",
    password="JMPog04EGI2MVcbO3HDPC9clDNyztfBX",
)

# Redis list names
redis_lists = ['amazon', 'flipkart', 'ajio']


def format_phone_number(phone_number):
    """
    Format phone number according to the rules:
    - If length > 10, remove first two digits

    Args:
        phone_number (str): The phone number to format

    Returns:
        str: Formatted phone number
    """
    if len(phone_number) > 10:
        return phone_number[2:]
    return phone_number


def push_to_redis(file_path):
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
            for row in csv_reader:
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

    # Example usage


if __name__ == "__main__":
    # file_path = input("Enter the path to the CSV file: ")
    push_to_redis("phone-numbers-csv.csv")