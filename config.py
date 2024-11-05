import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    # Path for SQLite database file
    SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH', 'recrutech.db')  # Default to `recrutech.db` in the current directory
