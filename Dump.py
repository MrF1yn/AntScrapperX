import csv
import psycopg2


def create_table_if_not_exists(connection):
    """
    Create the phone_numbers table if it does not exist.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS phone_numbers (
        id SERIAL PRIMARY KEY,
        phone_number VARCHAR(15) NOT NULL
    );
    """
    with connection.cursor() as cursor:
        cursor.execute(create_table_query)
        connection.commit()


def update_phone_numbers_in_batches(file_path, batch_size, connection):
    """
    Reads phone numbers from a CSV file in batches and updates them in the phone_numbers table.

    Args:
        file_path (str): Path to the CSV file.
        batch_size (int): Number of records to process in each batch.
        connection (psycopg2 connection): Connection to the PostgreSQL database.
    """
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Skip header row if present
        headers = next(csv_reader, None)
        if headers and not headers[0].isdigit():
            print("Skipping header row.")

        batch = []
        for row in csv_reader:
            if len(row) != 1:
                print(f"Skipping malformed row: {row}")
                continue

            batch.append(row[0])

            if len(batch) >= batch_size:
                insert_batch(connection, batch)
                batch = []

        # Insert any remaining records
        if batch:
            insert_batch(connection, batch)


def insert_batch(connection, batch):
    """
    Inserts a batch of phone numbers into the phone_numbers table.

    Args:
        connection (psycopg2 connection): Connection to the PostgreSQL database.
        batch (list): List of phone numbers to insert.
    """
    insert_query = """
    INSERT INTO phone_numbers (phone_number) VALUES (%s)
    ON CONFLICT DO NOTHING;
    """
    with connection.cursor() as cursor:
        cursor.executemany(insert_query, [(phone,) for phone in batch])
        connection.commit()


if __name__ == "__main__":
    # Database connection URL
    db_url = "postgresql://postgres:qS1hAyZFcQFqrre6@db.lthjdpnfcewonemuleed.supabase.co:5432/postgres"

    csv_file_path = 'phone-numbers-csv.csv'  # Path to your CSV file
    batch_size = 100  # Number of records to process in each batch

    try:
        with psycopg2.connect(db_url) as conn:
            create_table_if_not_exists(conn)
            update_phone_numbers_in_batches(csv_file_path, batch_size, conn)
            print("Phone numbers updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
