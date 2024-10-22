import requests
import psycopg2
from psycopg2.extras import execute_values

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="your_db",
    user="your_user",
    password="your_password",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()