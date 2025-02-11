import os
import sys
from data_loading import *
from data_extraction import generate_csv
from data_transformation import transform_csv
from sql_queries import run_queries

def main():
    # 1. Generate data
    generate_csv("users.csv", num_records=1500)
    
    # 2. Transform data
    transform_csv("users.csv", "users_transformed.csv")
    
    # 3. Database credentials (could read from environment variables)
    db_name = os.environ.get("DB_NAME", "mydb")
    db_user = os.environ.get("DB_USER", "postgres")
    db_pass = os.environ.get("DB_PASS", "password")
    db_host = os.environ.get("DB_HOST", "db")
    db_port = os.environ.get("DB_PORT", "5432")

    # 4. Create table
    create_table(db_name, db_user, db_pass, db_host, db_port)

    # 5. Insert data into table
    insert_data(db_name, db_user, db_pass, db_host, db_port, csv_file="users_transformed.csv")

    # 6. Run queries
    run_queries(db_name, db_user, db_pass, db_host, db_port)

if __name__ == "__main__":
    try:
        main()
        print("ETL process completed successfully.")
    except Exception as e:
        print(f"ETL failed: {e}", file=sys.stderr)
        sys.exit(1)