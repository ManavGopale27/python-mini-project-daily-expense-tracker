# gui.py
# Contains the main tkinter GUI class  (GUI requirement)

import tkinter as tk
from tkinter import messagebox
import threading
import datetime

from expense   import Expense
from queue_ds  import CustomQueue
from database  import save_expense_to_db, DB_NAME
from chart     import show_pie_chart
from clock     import run_clock


class ExpenseApp:
    """
    The main application class.
    Builds the GUI and wires up all the functionality.
    """

    def __init__(self, root):
        self.root = root
        self.root.title('Personal Expense Logger')
        self.root.geometry('500x440')
        self.root.minsize(420, 400)

        # This queue will hold expenses that are not yet saved to DB
        self.pending_queue = CustomQueue()

        # Build all the widgets
        self.build_ui()

        # Start the clock thread (daemon=True so it dies with the app)
        self.stop_clock = threading.Event()
        clock_thread = threading.Thread(
            target=run_clock,
            args=(self.clock_label, self.stop_clock),
            daemon=True
        )
        clock_thread.start()

        # Intercept the window close button so we stop the thread properly
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)

    # ----------------------------------------------------------
    def build_ui(self):
        """Builds and arranges all tkinter widgets."""

        # ---- Top bar: title on left, clock on right ----
        top_bar = tk.Frame(self.root)
        top_bar.pack(fill='x', padx=10, pady=(10, 0))

        tk.Label(
            top_bar,
            text='Personal Expense Logger',
            font=('Arial', 14, 'bold')
        ).pack(side='left')

        # Clock label - gets updated by background thread every second
        self.clock_label = tk.Label(
            top_bar,
            text='  --:--:-- --  ',
            font=('Courier', 10),
            relief='sunken',
            bd=1
        )
        self.clock_label.pack(side='right')

        # ---- Input section ----
        input_frame = tk.LabelFrame(self.root, text='Add New Expense', padx=12, pady=10)
        input_frame.pack(padx=12, pady=8, fill='x')

        # Row 0 - Date
        tk.Label(input_frame, text='Date  (DD-MM-YYYY) :').grid(
            row=0, column=0, sticky='w', pady=5
        )
        self.entry_date = tk.Entry(input_frame, width=28)
        self.entry_date.grid(row=0, column=1, pady=5, padx=6)
        # Pre-fill with today's date
        self.entry_date.insert(0, datetime.date.today().strftime('%d-%m-%Y'))

        # Row 1 - Category
        tk.Label(input_frame, text='Category           :').grid(
            row=1, column=0, sticky='w', pady=5
        )
        self.entry_category = tk.Entry(input_frame, width=28)
        self.entry_category.grid(row=1, column=1, pady=5, padx=6)

        # Row 2 - Amount
        tk.Label(input_frame, text='Amount  (Rs.)      :').grid(
            row=2, column=0, sticky='w', pady=5
        )
        self.entry_amount = tk.Entry(input_frame, width=28)
        self.entry_amount.grid(row=2, column=1, pady=5, padx=6)

        # ---- Buttons ----
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=6)

        tk.Button(
            btn_frame, text='Add to Queue',
            width=15, command=self.add_to_queue
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            btn_frame, text='Save All',
            width=15, command=self.save_all
        ).grid(row=0, column=1, padx=8)

        tk.Button(
            btn_frame, text='Show Chart',
            width=15, command=show_pie_chart
        ).grid(row=0, column=2, padx=8)

        # ---- Status label ----
        self.status_label = tk.Label(
            self.root,
            text='Queue is empty.',
            font=('Arial', 9),
            fg='gray'
        )
        self.status_label.pack()

        # ---- Pending queue listbox ----
        list_frame = tk.LabelFrame(
            self.root,
            text='Pending Queue  (not yet saved to database)',
            padx=6, pady=6
        )
        list_frame.pack(padx=12, pady=6, fill='both', expand=True)

        # Scrollbar for the listbox
        scrollbar = tk.Scrollbar(list_frame, orient='vertical')
        scrollbar.pack(side='right', fill='y')

        self.queue_listbox = tk.Listbox(
            list_frame,
            font=('Courier', 9),
            yscrollcommand=scrollbar.set
        )
        self.queue_listbox.pack(fill='both', expand=True)
        scrollbar.config(command=self.queue_listbox.yview)

    # ----------------------------------------------------------
    def add_to_queue(self):
        """
        Reads the three input fields, validates them,
        creates an Expense object, and enqueues it.
        The item is shown in the listbox but NOT saved yet.
        """
        date_val     = self.entry_date.get().strip()
        category_val = self.entry_category.get().strip()
        amount_text  = self.entry_amount.get().strip()

        # Basic validation - check empty fields
        if date_val == '' or category_val == '' or amount_text == '':
            messagebox.showwarning('Empty Fields', 'Please fill in all three fields.')
            return

        # Check that amount is actually a number
        try:
            amount_val = float(amount_text)
        except ValueError:
            messagebox.showerror('Invalid Amount', 'Amount must be a number.\nExample: 150 or 99.50')
            return

        if amount_val <= 0:
            messagebox.showerror('Invalid Amount', 'Amount must be greater than 0.')
            return

        # Create an Expense object and put it in the queue
        new_expense = Expense(date_val, category_val, amount_val)
        self.pending_queue.enqueue(new_expense)

        # Show it in the listbox
        self.queue_listbox.insert(tk.END, str(new_expense))

        # Update the status message
        count = self.pending_queue.size
        self.status_label.config(
            text=f'{count} item(s) in queue.  Click Save All to save to database.',
            fg='blue'
        )

        # Clear category and amount fields for next entry, keep date
        self.entry_category.delete(0, tk.END)
        self.entry_amount.delete(0, tk.END)
        self.entry_category.focus()

    # ----------------------------------------------------------
    def save_all(self):
        """
        Dequeues every expense from the CustomQueue one by one
        and saves each one into the SQLite database.
        """
        if self.pending_queue.is_empty():
            messagebox.showinfo('Nothing to Save', 'The queue is empty.\nAdd some expenses first.')
            return

        saved_count = 0

        # Keep dequeuing until the queue is completely empty
        while not self.pending_queue.is_empty():
            expense = self.pending_queue.dequeue()
            save_expense_to_db(expense)
            saved_count += 1

        # Clear the listbox display
        self.queue_listbox.delete(0, tk.END)

        # Reset the status label
        self.status_label.config(text='Queue is empty.', fg='gray')

        messagebox.showinfo(
            'Saved Successfully',
            f'{saved_count} expense(s) saved to {DB_NAME}.'
        )

    # ----------------------------------------------------------
    def on_close(self):
        """Called when the user clicks the X button to close the window."""
        # Tell the clock thread to stop before destroying the window
        self.stop_clock.set()
        self.root.destroy()
