from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# Establish connection to postgres database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create session to talk to database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that all models we create will extend from
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# # use with statement to establish connection with database (since connection can fail)
# # connect to database
# try:    
#     conn = psycopg.connect(f"dbname={settings.database_name} user={settings.database_username} password={settings.database_password} 
#     host={settings.database_hostname}", row_factory= psycopg.rows.dict_row)
#     cursor = conn.cursor()
#     print('Database connection successful')
# except Exception as error:
#     print('Connection Failed')
#     print('Error: ', error)
    
  