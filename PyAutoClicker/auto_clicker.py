import pyautogui
import time
import threading
from tkinter import *
import tkinter.font as font
import threading
from tkinter import messagebox

is_running = False

# Auto-clicker function
def auto_clicker(clicks, interval, start_event, stop_event):
    global is_running
    status_label.config(text=f"Starting... You requested {clicks} clicks with an interval of {interval} seconds.")
    for _ in range(clicks):
        if stop_event.is_set():
            break
        pyautogui.click()
        status_label.config(text="Click")
        time.sleep(interval)
    start_event.clear()
    is_running = False
    status_label.config(text="Auto-clicker stopped.")

# Start the auto-clicker
def start_clicker():
    global is_running
    if is_running:
        status_label.config(text="Auto-clicker is already running.")
        return
    try:
        clicks = int(clicks_entry.get())
        interval = float(interval_entry.get())
        delay = float(delay_entry.get())
        stop_event.clear()
        start_event.set()
        is_running = True
        threading.Thread(target=lambda: start_after_delay(clicks, interval, delay), daemon=True).start()
        status_label.config(text=f"Auto-clicker will start in {delay} seconds.")
    except ValueError:
        status_label.config(text="Please enter valid numbers.")

def start_after_delay(clicks, interval, delay):
    time.sleep(delay) 
    if not stop_event.is_set(): 
        threading.Thread(target=auto_clicker, args=(clicks, interval, start_event, stop_event), daemon=True).start()
    else:
        start_event.clear()
        is_running = False
        print("Auto-clicker stopped before starting due to stop command.")

def stop_clicker():
    global is_running
    if not is_running:
        messagebox.showinfo("Auto Clicker", "Auto-clicker is not running.")
        return
    stop_event.set()
    start_event.clear()
    is_running = False
    messagebox.showinfo("Auto Clicker", "Auto-clicker has stopped.")

# GUI setup
root = Tk()
root.title("Auto Clicker 🖱️")
root.geometry("400x250") 
root.configure(bg='#ADD8E6')  

# Custom font
myFont = font.Font(family='Helvetica', size=12, weight='bold')

Label(root, text="Delay Before Start (seconds): ⏳", bg='#ADD8E6', fg='black', font=myFont).pack()
delay_entry = Entry(root, font=myFont)
delay_entry.pack()

# Label and Entry for Number of Clicks
Label(root, text="Number of Clicks: 🖱️", bg='#ADD8E6', fg='black', font=myFont).pack()
clicks_entry = Entry(root, font=myFont)
clicks_entry.pack()

# Label and Entry for Interval Between Clicks
Label(root, text="Interval Between Clicks (seconds): ⏱️", bg='#ADD8E6', fg='black', font=myFont).pack()
interval_entry = Entry(root, font=myFont)
interval_entry.pack()

status_label = Label(root, text="Status: Ready", bg='#ADD8E6', fg='black', font=font.Font(size=10))
status_label.pack()

# Start and Stop Events
start_event = threading.Event()
stop_event = threading.Event()

# Example of adding a button with custom colors and emoji
start_button = Button(root, text="Start 🚀", command=start_clicker, bg='#90EE90', fg='black', font=myFont)  
start_button.pack(pady=5)

stop_button = Button(root, text="Stop 🛑", command=stop_clicker, bg='#FF6347', fg='black', font=myFont)  
stop_button.pack(pady=5)

root.mainloop()