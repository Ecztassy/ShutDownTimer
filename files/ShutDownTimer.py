import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import time
from ttkthemes import ThemedTk

def cancel_shutdown():
    global canceled
    canceled = True
    cancel_label.config(text="Shutdown canceled", fg="red")

def countdown_and_shutdown():
    global total_seconds, canceled
    try:
        for i in range(int(total_seconds.get()), -1, -1):
            hours, remainder = divmod(i, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left_label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}", font=("Arial", 28))
            root.update()
            if canceled:
                cancel_label.config(text="Shutdown canceled", fg="red")
                break
            time.sleep(1)

        if not canceled:
            time_left_label.config(text="Shutting down...", font=("Arial", 28))
            subprocess.run(f"shutdown /s /t 1", shell=True, check=True)  # Change the time to 1 second for testing
    except Exception as e:
        print("Error occurred during shutdown:", e)

def start_shutdown_timer():
    global total_seconds, canceled
    hours = int(hours_entry.get()) if hours_entry.get() else 0
    minutes = int(minutes_entry.get()) if minutes_entry.get() else 0
    seconds = int(seconds_entry.get()) if seconds_entry.get() else 0

    total_seconds.set(hours * 3600 + minutes * 60 + seconds)
    canceled = False
    threading.Thread(target=countdown_and_shutdown).start()

# Create the Tkinter window
root = ThemedTk(theme="arc")
root.title("Shutdown Timer")
root.geometry("500x300")  # Set a fixed window size

# Add a background image as the background of the entire window
background_image = tk.PhotoImage(file="C:\\Users\\Admin\\Desktop\\discordbot\\200.gif")  # Replace "background.png" with your image file
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Create total_seconds as a global StringVar
total_seconds = tk.StringVar()

# Create labels and entry widgets for hours, minutes, and seconds
hours_label = ttk.Label(root, text="Hours:", font=("Arial", 14))
hours_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

hours_entry = ttk.Entry(root, width=5, font=("Arial", 14))
hours_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

minutes_label = ttk.Label(root, text="Minutes:", font=("Arial", 14))
minutes_label.grid(row=0, column=2, padx=10, pady=10, sticky='e')

minutes_entry = ttk.Entry(root, width=5, font=("Arial", 14))
minutes_entry.grid(row=0, column=3, padx=10, pady=10, sticky='w')

seconds_label = ttk.Label(root, text="Seconds:", font=("Arial", 14))
seconds_label.grid(row=0, column=4, padx=10, pady=10, sticky='e')

seconds_entry = ttk.Entry(root, width=5, font=("Arial", 14))
seconds_entry.grid(row=0, column=5, padx=10, pady=10, sticky='w')

# Create buttons to start the timer and cancel (with rounded corners)
start_button = ttk.Button(root, text="Start", command=start_shutdown_timer, style="TButton")
start_button.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky='ew')

cancel_button = ttk.Button(root, text="Cancel", command=cancel_shutdown, style="TButton")
cancel_button.grid(row=1, column=3, columnspan=2, padx=10, pady=10, sticky='ew')

# Create labels to display time left for shutdown and cancellation message
time_left_label = tk.Label(root, text="", font=("Arial", 28), bg='white')
time_left_label.grid(row=2, column=0, columnspan=6, pady=10, sticky='ew')

cancel_label = tk.Label(root, text="", font=("Arial", 28), fg="red", bg='white')
cancel_label.grid(row=3, column=0, columnspan=6, pady=10, sticky='ew')

# Center the countdown label horizontally
root.grid_rowconfigure((2, 3), weight=1)
root.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

# Run the Tkinter main loop
root.mainloop()
