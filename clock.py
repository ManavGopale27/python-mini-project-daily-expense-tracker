# clock.py
# Contains the live clock thread function  (Multithreading requirement)

import time
import datetime


def run_clock(label, stop_flag):
    """
    Runs in a background thread. Updates the clock label every second.
    We use label.after(0, ...) because tkinter is NOT thread-safe.
    Never modify a widget directly from a non-main thread.
    """
    while not stop_flag.is_set():
        now  = datetime.datetime.now()
        text = now.strftime('  %I:%M:%S %p  ')

        # Schedule the label update safely on the main thread
        label.after(0, lambda t=text: label.config(text=t))

        time.sleep(1)
