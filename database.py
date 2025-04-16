import sqlite3
from logger import logger

from dotenv import load_dotenv
import os

load_dotenv()

DB_PATH = os.getenv('DB_PATH')


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            xpath TEXT NOT NULL,
            price TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    logger.info("Database initialized")


def save_to_db(user_id, title, url, xpath, price):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO products (user_id, title, url, xpath, price)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, title, url, xpath, price))
        conn.commit()
        logger.info(f"Data saved for user {user_id}: {title}")
    except Exception as e:
        logger.error(f"Error saving to DB: {e}")
    finally:
        conn.close()