import psycopg2
from psycopg2 import sql

def create_database():
    try:
        # Connect to the default 'postgres' database to issue the CREATE DATABASE command
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="data wizards", 
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        
        cursor = conn.cursor()
        
        # Check if tutor_db already exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'tutor_db'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(sql.SQL("CREATE DATABASE tutor_db"))
            print("Successfully created database 'tutor_db'.")
        else:
            print("Database 'tutor_db' already exists.")
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Failed to create database: {e}")
        print("\nPlease ensure PostgreSQL is running and the password for the 'postgres' user is 'postgres'.")
        print("If your password is different, please update this script or run: psql -U postgres -c 'CREATE DATABASE tutor_db;'")

if __name__ == "__main__":
    create_database()
