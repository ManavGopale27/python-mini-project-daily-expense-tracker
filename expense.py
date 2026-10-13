# expense.py
# Contains the Expense class  (OOP requirement)

class Expense:
    """
    A simple class to hold one expense record.
    Has three fields: date, category, and amount.
    """

    def __init__(self, date, category, amount):
        self.date     = date
        self.category = category
        self.amount   = amount   # stored as a float

    # This makes it easy to print an Expense object
    def __str__(self):
        return f"{self.date}  |  {self.category}  |  Rs. {self.amount:.2f}"
