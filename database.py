# database.py
# Contains all SQLite3 database functions  (Database requirement)

import sqlite3

DB_NAME = 'expenses.db'


def setup_database():
    """
    Creates the expenses table if it does not already exist.
    Called once when the program starts.
    """
    conn   = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            date     TEXT,
            category TEXT,
            amount   REAL
        )
    """)

    conn.commit()
    conn.close()


def save_expense_to_db(expense):
    """
    Inserts a single Expense object into the database.
    """
    conn   = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)',
        (expense.date, expense.category, expense.amount)
    )

    conn.commit()
    conn.close()
