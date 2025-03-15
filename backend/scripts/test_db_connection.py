import os
import psycopg2

# Get database credentials from environment variables
db_host = os.getenv("POSTGRES_SERVER")
db_port = os.getenv("POSTGRES_PORT", "5432")
db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")

# Construct the PostgreSQL connection string
db_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

print(f"🔍 Checking database connection to {db_uri}...")

try:
    conn = psycopg2.connect(db_uri)
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    print("Database connection successful!")
    conn.close()
except Exception as e:
    print("Database connection failed: {e}")
