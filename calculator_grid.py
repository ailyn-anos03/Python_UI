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


entry = tk.Entry(window, textvar=result, font=("Arial", 20), justify="right")
entry.grid(row=0, column=0, columnspan=4)


buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
]


for text, row, col in buttons:
    button = tk.Button(window, text=text, font=("Arial", 20), width=5, height=2)
    button.grid(row=row, column=col, padx=5, pady=5)
    button.config(command=lambda t=text: result.set(result.get() + t) if t != "=" else calculate())

# Run the application
window.mainloop()
