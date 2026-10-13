# main.py
# ============================================================
#  Personal Expense Logger  -  Modular Version
#  Mini Project - Python Programming (Semester 3 / 4)
#  Student Name : [Your Name]
#  Roll Number  : [Your Roll No]
#  Date         : 13-10-2026
# ============================================================
#
#  Project Structure  (Modules and Packages):
#   main.py      - Entry point. Run this file to start the app.
#   expense.py   - Expense class                  (OOP)
#   queue_ds.py  - Node + CustomQueue             (Custom DS)
#   database.py  - setup_database, save_expense   (SQLite3)
#   chart.py     - show_pie_chart                 (Visualization)
#   clock.py     - run_clock thread function      (Multithreading)
#   gui.py       - ExpenseApp window class        (GUI / tkinter)
# ============================================================

import tkinter as tk

from database import setup_database
from gui      import ExpenseApp


if __name__ == '__main__':
    # Step 1: Make sure the database and table exist
    setup_database()

    # Step 2: Create the main window and start the app
    root = tk.Tk()
    app  = ExpenseApp(root)
    root.mainloop()
