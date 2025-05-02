import tkinter as tk
from tkinter import ttk


window = tk.Tk()
window.title("Tkinter Tabs Example")

# Create a Notebook widget (tab container)
notebook = ttk.Notebook(window)

# Create frames for the tabs
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(tab1, text="Tab 1")
notebook.add(tab2, text="Tab 2")
notebook.add(tab3, text="Tab 3")

notebook.pack(expand=True, fill="both")

# Function for button click event
def on_button_click(tab_name):
    print(f"Button clicked in {tab_name}")

# Adding widgets to Tab 1
label1 = ttk.Label(tab1, text="This is Tab 1")
label1.pack(pady=10)
button1 = ttk.Button(tab1, text="Go to Tab 2", command=lambda: notebook.select(tab2))
button1.pack(pady=5)

# Adding widgets to Tab 2
label2 = ttk.Label(tab2, text="This is Tab 2")
label2.pack(pady=10)
button2 = ttk.Button(tab2, text="Go to Tab 1", command=lambda: notebook.select(tab1))
button2.pack(pady=5)

# Adding widgets to Tab 3
label3 = ttk.Label(tab3, text="This is Tab 3")
label3.pack(pady=10)
button3 = ttk.Button(tab3, text="Go to Tab 3", command=lambda: notebook.select(tab3))
button3.pack(pady=5)


window.mainloop()

