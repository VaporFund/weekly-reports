import os

from dotenv import load_dotenv

load_dotenv()

dbname = os.getenv("DBNAME")
dbuser = os.getenv("DBUSER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")

import psycopg2
import csv


def fetch_data_and_save_to_csv(db_params, sql_query, csv_filepath):
    """
    Fetches data from a PostgreSQL database using a given SQL query
    and saves the results to a CSV file.

    Args:
        db_params (dict): Dictionary containing database connection parameters
                          (dbname, user, password, host, port).
        sql_query (str): The SQL query to execute.
        csv_filepath (str): The path where the CSV file will be saved.
    """
    conn = None
    try:
        # 1. Connect to the PostgreSQL database
        print(f"Connecting to database: {db_params.get('dbname')}...")
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        print("Connection successful.")

        # 2. Execute the SQL query
        print(f"Executing query: {sql_query}")
        cur.execute(sql_query)
        print("Query executed.")

        # 3. Fetch all results
        results = cur.fetchall()
        print(f"Fetched {len(results)} rows.")

        if not results:
            print("No data returned from the query.")
            return

        # 4. Get column headers
        column_names = [desc[0] for desc in cur.description]

        # 5. Write data to a CSV file
        print(f"Writing data to {csv_filepath}...")
        with open(csv_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write the header row
            csv_writer.writerow(column_names)
            # Write the data rows
            csv_writer.writerows(results)
        print(f"Data successfully saved to {csv_filepath}")

    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL or executing query: {error}")
    finally:
        # Close the database connection
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed.")


def main_download_csv():
    """Download the csv file."""
    # --- Configuration ---
    database_parameters = {
        "dbname": dbname,
        "user": dbuser,
        "password": password,
        "host": host,  # e.g., 'localhost' or an IP address
        "port": port  # e.g., '5432' for PostgreSQL
    }

    # The SQL query you provided
    query = """
    SELECT *
    FROM price_snapshots
    WHERE "timestamp" >= NOW() - INTERVAL '168 hours'
      AND token_symbol = 'uSOL'
      AND profit_percentage > 0
    ORDER BY token_symbol, "timestamp";
    """

    # Desired output CSV file path
    output_csv_file = "price_snapshots_usol.csv"

    # --- Execute ---
    fetch_data_and_save_to_csv(database_parameters, query, output_csv_file)


if __name__ == "__main__":
    main_download_csv()
