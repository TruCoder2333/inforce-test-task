import psycopg2
import psycopg2.extensions
import csv

def create_db(dbname, user, password, host="localhost", port="5432"):
    conn = psycopg2.connect(
        dbname="postgres",
        user=user,
        password=password,
        host=host,
        port=port
    )

    # Turn on autocommit explicitly
    conn.autocommit = True
    cur = conn.cursor()

    # Check if the database already exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname=%s;", (dbname,))
    exists = cur.fetchone()

    if not exists:
        print(f"Creating database {dbname}...")
        cur.execute(f'CREATE DATABASE "{dbname}";')
    else:
        print(f"Database {dbname} already exists")

    cur.close()
    conn.close()

def create_table(dbname, user, password, host="localhost", port="5432"):
    table_creation_query = """
    CREATE TABLE IF NOT EXISTS users_transformed (
        user_id INT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        signup_date DATE NOT NULL,
        domain TEXT NOT NULL
    );
    """

    with psycopg2.connect(
        dbname=dbname, 
        user=user,
        password=password,
        host=host,
        port=port
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(table_creation_query)
            conn.commit()
            print("Table created, all good")

def insert_data(
        dbname, 
        user, 
        password, 
        host="localhost", 
        port="5432",
        csv_file="users_transformed.csv"
    ):
    with psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    ) as conn:
        with conn.cursor() as cur:
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                insert_query = """
                    INSERT INTO users_transformed (user_id, name, email, signup_date, domain)        
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (user_id)
                    DO NOTHING
                    """
                
                for row in reader:
                    user_id = int(row["user_id"])
                    name = row["name"]
                    email = row["email"]
                    signup_date = row["signup_date"]
                    domain = row["domain"]

                    cur.execute(insert_query, (user_id, name, email, signup_date, domain))

            conn.commit()
            print("Data inserted into the table")

if __name__=="__main__":
    DB_NAME = "mydb"
    DB_USER = "postgres"
    DB_PASS = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    create_db(DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT)

    create_table(DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT)

    insert_data(DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT, csv_file="users_transformed.csv")