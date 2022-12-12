import psycopg
import sys

# class that implements a psycopg connection to database
class Database:
    def __init__(self):
        self.conn = self.connect()
        self.cursor = self.conn.cursor()
    
    def connect(self):
        print("Connecting to PostgreSQL Database")
        try:
            conn = psycopg.connect("dbname=python-api user=postgres password=mscriket007 host=127.0.0.1", row_factory= psycopg.rows.dict_row)
        except psycopg.OperationalError as e:
            print(f"Could not connect to Database: {e}")
            sys.exit(1)
        print("Connected")
        return conn

db = Database()