import psycopg2

def show_query_results(cursor, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    print("Results")
    for row in rows:
        print(row)
    print()

def run_queries(
        dbname, 
        user, 
        password,
        host="localhost",
        port="5432"
    ):
    conn = psycopg2.connect(
        dbname=dbname,
        user=user, 
        password=password,
        host=host,
        port=port
    )
    try:
        with conn.cursor() as cur:

            # 1
            print("Query 1")
            q1 = """
                SELECT signup_date, COUNT(*) as user_count
                FROM users_transformed
                GROUP BY signup_date
                ORDER BY signup_date;
            """
            show_query_results(cur, q1)

            # 2
            print("Query 2")
            q2 = """
                SELECT DISTINCT domain 
                FROM users_transformed; 
            """
            show_query_results(cur, q2)

            # 3
            print("Query 3")
            q3 = """
                SELECT *
                FROM users_transformed
                WHERE signup_date >= CURRENT_DATE - INTERVAL '7 days'
            """
            show_query_results(cur, q3)

            # 4
            print("Query 4")
            q4 = """
                WITH domain_counts AS (
                    SELECT 
                        domain, 
                        COUNT(*) AS domain_count
                    FROM users_transformed
                    GROUP BY domain
                ),
                max_count AS (
                    SELECT MAX(domain_count) AS max_domain_count
                    FROM domain_counts
                )
                SELECT u.*
                FROM users_transformed u
                JOIN domain_counts dc 
                    ON u.domain = dc.domain
                JOIN max_count mc
                    ON dc.domain_count = mc.max_domain_count;
            """
            show_query_results(cur, q4)

            # 5
            print("Query 5")
            test_query = """
                SELECT COUNT(*) FROM users_transformed
            """
            print("Number of rows before deletion")
            show_query_results(cur, test_query)

            q5 = """
                DELETE FROM users_transformed
                WHERE domain NOT IN ('gmail.com', 'yahoo.com', 'example.com');
            """
            cur.execute(q5)
            print("Number of rows after deletion")
            show_query_results(cur, test_query)
    finally:
        conn.close()

if __name__=="__main__":
    run_queries(
        dbname="mydb",
        user="postgres",
        password="DurexL0ve",
        host="localhost",
        port="5432"
    )