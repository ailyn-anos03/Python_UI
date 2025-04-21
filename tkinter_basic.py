import tkinter as tk
from tkinter import ttk


window = tk.Tk()
window.title("Anos Page")
window.geometry("500x550")
window.configure(bg="pink")


label = ttk.Label(master = window, text = "Welcome to My Page", font = "Arial 12 italic", background= "pink")
label.pack( padx=10, pady=10)

button = ttk.Button(master = window, text = "Close", command = window.destroy)
button.pack( padx=10, pady=10)

textbox = ttk.Entry(master=window, font= "Calibri 14 bold")
textbox.pack( padx=10, pady=10)

window.mainloop()
