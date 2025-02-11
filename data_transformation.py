import re
import csv
from datetime import datetime

EMAIL_REGEX = re.compile(
    r"^(?!.*\.\.)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)

def transform_csv(input_file, output_file):
    with open(input_file, mode="r", encoding="utf-8") as infile, \
         open(output_file, mode="w", encoding="utf-8", newline="") as outfile:
         reader = csv.DictReader(infile)
         fieldnames = reader.fieldnames + ["domain"]
         writer = csv.DictWriter(outfile, fieldnames=fieldnames)
         writer.writeheader()

         for row in reader:
            email = row["email"].strip()
            
            if not re.match(EMAIL_REGEX, email):
                continue

            try:
                original_date = datetime.strptime(row["signup_date"], "%Y-%m-%d %H:%M:%S")
                row["signup_date"] = original_date.strftime("%Y-%m-%d")
            except ValueError:
                continue

            domain = email.split("@", 1)[1]
            row["domain"] = domain

            writer.writerow(row)

if __name__=="__main__":
    transform_csv("users.csv", "users_transformed.csv")
