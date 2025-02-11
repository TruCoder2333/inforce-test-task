Running docker files
From the project root directory (where docker-compose.yml is located), run:

docker-compose up --build

This will:

Build the Python app image using the Dockerfile.
Pull the PostgreSQL base image (postgres:16) if not present.
Run both containers:
db (PostgreSQL)
app (Python ETL)

Verifying the Containers
Check logs in your terminal to see if the ETL script completed successfully.
You can also open another terminal to run:

docker ps

You should see two running containers: one for db and one for app.

To stop the containers (in your current terminal session), press CTRL+C. Or run:

docker-compose down

-------------------------
Database schema

Column	        Type	Constraints	    Description
user_id	        INT	    PRIMARY KEY	    Unique user identifier
name	        TEXT	NOT NULL	    Full name
email	        TEXT	NOT NULL	    User's email address
signup_date	    DATE	NOT NULL	    Date (YYYY-MM-DD) when the user signed up
domain	        TEXT	NOT NULL	    Extracted email domain

Schema creation script
CREATE TABLE IF NOT EXISTS users_transformed (
    user_id INT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    signup_date DATE NOT NULL,
    domain TEXT NOT NULL
);

----------------------------
Assumptions
-Assumes user_id is unique for each user. The table uses INT PRIMARY KEY.

-The app container uses DB_HOST=db (the default service name in Docker Compose) to connect to the PostgreSQL container.

-The default credentials (POSTGRES_USER=postgres, 
POSTGRES_PASSWORD=password) are obviously insecure for production. Change them before deploying to a public environment.
