# chart.py
# Contains the pie chart function  (Data Visualization requirement)

import sqlite3
from tkinter import messagebox

import pandas as pd
import matplotlib.pyplot as plt

from database import DB_NAME


def show_pie_chart():
    """
    Reads all expense data from the SQLite database using pandas,
    groups by category, and shows a pie chart with matplotlib.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        df   = pd.read_sql_query('SELECT category, amount FROM expenses', conn)
        conn.close()

        # If the table is empty, warn the user
        if df.empty:
            messagebox.showinfo(
                'No Data',
                'No expenses saved yet.\nPlease add and save some expenses first.'
            )
            return

        # Group by category and sum the amounts
        grouped = df.groupby('category')['amount'].sum()

        # Draw the pie chart
        plt.figure(figsize=(6, 6))
        plt.pie(
            grouped,
            labels=grouped.index,
            autopct='%1.1f%%',
            startangle=90
        )
        plt.title('Expense Breakdown by Category')
        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror('Chart Error', f'Something went wrong:\n{e}')
