import csv
from faker import Faker

def generate_csv(filename, num_records=1000):
    fake = Faker()
    
    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        
        writer.writerow(["user_id", "name", "email", "signup_date"])
        
        for i in range(1, num_records + 1):
            user_id = i
            name = fake.name()  
            email = fake.email()  
            signup_date = fake.date_time_between(start_date='-2y', end_date='now')
            signup_date_str = signup_date.strftime("%Y-%m-%d %H:%M:%S")
            
            writer.writerow([user_id, name, email, signup_date_str])

if __name__ == "__main__":
    num_records = 4000
    generate_csv("users.csv", num_records)
    print(f"CSV file 'users.csv' has been generated with {num_records} records.")
