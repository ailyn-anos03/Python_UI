import tkinter as tk
from tkinter import ttk 


def calculate():
    try:
        result.set(eval(result.get()))
    except:
        result.set("Error")


window = tk.Tk()
window.title("Basic Calculator")

result = tk.StringVar()
entry1 = tk.Entry(window, textvar=result, font=("Arial", 20), justify="right")
entry1.grid(row=0, column=0, columnspan=4)

entry = tk.Entry(window, textvar=result, font=("Arial", 20), justify="right")
entry.grid(row=1, column=0, columnspan=4)

#List of buttons

buttons = [
    ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("/", 2, 3),
    ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("*", 3, 3),
    ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("-", 4, 3),
    ("0", 5, 0), (".", 5, 1), ("=", 5, 2), ("+", 5, 3),
]


for text, row, col in buttons:
    button = tk.Button(window, text=text, font=("Arial", 20), width=5, height=2)
    button.grid(row=row, column=col, padx=5, pady=5)
    button.config(command=lambda t=text: result.set(result.get() + t) if t != "=" else calculate())
    
window.mainloop()
