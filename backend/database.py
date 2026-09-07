import sqlite3
import os
from datetime import datetime


# Find the main H2S-SafeBand folder
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# Database folder
DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)


# Database file
DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "h2s.db"
)


def get_connection():

    # Create database folder if it doesn't exist
    os.makedirs(
        DATABASE_DIR,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def create_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            worker_id TEXT NOT NULL,

            worker_name TEXT NOT NULL,

            exposure REAL NOT NULL,

            status TEXT NOT NULL,

            confidence REAL,

            image_name TEXT,

            scan_time TEXT NOT NULL

        )
    """)

    connection.commit()

    connection.close()


def insert_scan(
    worker_id,
    worker_name,
    exposure,
    status,
    confidence,
    image_name
):

    connection = get_connection()

    cursor = connection.cursor()

    scan_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO scans
        (
            worker_id,
            worker_name,
            exposure,
            status,
            confidence,
            image_name,
            scan_time
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        worker_id,
        worker_name,
        exposure,
        status,
        confidence,
        image_name,
        scan_time
    ))

    connection.commit()

    connection.close()


def get_history():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM scans
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]