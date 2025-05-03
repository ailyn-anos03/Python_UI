import tkinter as tk
from tkinter import ttk
from openpyxl import load_workbook, Workbook
from datetime import datetime
from tkinter import messagebox

window = tk.Tk()
window.title("Inventory Manager")
# window.title("Inventory Management")
window.configure(bg="AntiqueWhite2")

notebook = ttk.Notebook(window)

tab1 = tk.Frame(notebook, bg="AntiqueWhite2")
tab2 = tk.Frame(notebook, bg="AntiqueWhite2")
tab3 = tk.Frame(notebook, bg="AntiqueWhite2")

notebook.add(tab1, text="Home")
notebook.add(tab2, text="Input")
notebook.add(tab3, text="Hisory")
style = ttk.Style()
style.theme_use("clam")  

# Configure the notebook tabs
style.configure("TNotebook", background="RosyBrown3", bordercolor="black")  
style.configure("TNotebook.Tab", background="AntiqueWhite3", foreground="black")
style.map("TNotebook.Tab", background=[("selected", "AntiqueWhite2")], foreground=[("selected", "black")])  

notebook.grid(sticky="nsew")

# Make the notebook stretchable
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

try:
    wb = load_workbook("inventory.xlsx")
except FileNotFoundError:
    wb = Workbook()
    ws = wb.active
    ws.append(["Item", "Quantity", "Price"])  
    wb.save("inventory.xlsx")

ws = wb.active
selected_item_index = None 


def on_button_click(tab_name):
    print(f"Button clicked in {tab_name}")


def add_item():
    item, quantity, price = entry_item.get(), entry_quantity.get(), entry_price.get()
    if item and quantity and price:
        ws.insert_rows(2)  # Insert a new row at the top (after headers)
        ws.cell(row=2, column=1, value=item)
        ws.cell(row=2, column=2, value=quantity)
        ws.cell(row=2, column=3, value=price)
        wb.save("inventory.xlsx")
        tree.insert("", "0", values=(item, quantity, price))  # Insert at the top of the Treeview
        clear_entries()
        update_total()  # Update total after adding an item

def view_data():
    tree.delete(*tree.get_children())
    for row_index, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        tree.insert("", "end", values=row, iid=str(row_index))  # Assign row index as ID
def delete_item():
    global selected_item_index
    selected = tree.selection()
    if selected:
        row_index = int(selected[0])  
        ws.delete_rows(row_index)  
        wb.save("inventory.xlsx")
        tree.delete(selected[0])  
        selected_item_index = None  
        update_total()  
        selected_item_index = None  

def edit_item():
    global selected_item_index
    selected = tree.selection()
    if selected:
        selected_item_index = int(selected[0])  
        values = tree.item(selected[0], "values")
        entry_item.delete(0, tk.END)
        entry_item.insert(0, values[0])
        entry_quantity.delete(0, tk.END)
        entry_quantity.insert(0, values[1])
        entry_price.delete(0, tk.END)
def update_item():
    global selected_item_index
    if selected_item_index:
        new_values = (entry_item.get(), entry_quantity.get(), entry_price.get())
        if all(new_values):
            tree.item(str(selected_item_index), values=new_values) 
            ws[selected_item_index][0].value = new_values[0]  
            ws[selected_item_index][1].value = new_values[1]
            ws[selected_item_index][2].value = new_values[2]
            wb.save("inventory.xlsx")
            clear_entries()
            selected_item_index = None 
            update_total() 
            clear_entries()
            selected_item_index = None 

def clear_entries():
    entry_item.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_price.delete(0, tk.END)



# Tab 1 - Home

label1 = tk.Label(tab1, text="Inventory Management", bg="AntiqueWhite2", font="Arial 14 bold")
label1.grid(row=0, column=0, padx=10, pady=10)

button_list = [
    ("Inventory", lambda: notebook.select(tab2), "raised", "RosyBrown2"),
    ("History", lambda: notebook.select(tab3), "raised", "RosyBrown2"),
]

for i, (text, command, relief, bg) in enumerate(button_list, start=1):
    button = tk.Button(tab1, text=text, command=command, relief=relief, bg=bg)
    button.grid(row=i, column=0, padx=10, pady=5, sticky="we")
 
    

#Tab 2 - Input

tk.Label(tab2, text="Item", bg="AntiqueWhite2", font="Calibri 11").grid(row=0, column=0, sticky="w")
tk.Label(tab2, text="Quantity", bg="AntiqueWhite2", font="Calibri 11").grid(row=1, column=0, sticky="w")
tk.Label(tab2, text="Price", bg="AntiqueWhite2", font="Calibri 11").grid(row=2, column=0, sticky="w")

entry_item, entry_quantity, entry_price = tk.Entry(tab2, font="Times 11", justify="left"), tk.Entry(tab2, font="Times 11", justify="left"), tk.Entry(tab2, font="Times 11", justify="left")

entry_item.grid(row=0, column=1, sticky="we")
entry_quantity.grid(row=1, column=1,  sticky="we")
entry_price.grid(row=2, column=1, sticky="we")

tk.Button(tab2, text="Add", command=add_item, bg="AntiqueWhite2", relief="flat", font="Arial 10").grid(row=4, column=0, pady=5, sticky="we")
tk.Button(tab2, text="Refresh", command=view_data, bg="AntiqueWhite2", relief="flat",font="Arial 10").grid(row=4, column=1, pady=5, sticky="we")
tk.Button(tab2, text="Edit", command=edit_item, bg="AntiqueWhite2", relief="flat",font="Arial 10").grid(row=4, column=2, pady=5, sticky="we")
tk.Button(tab2, text="Delete", command=delete_item, bg="AntiqueWhite2", relief="flat",font="Arial 10").grid(row=4, column=3, pady=5, sticky="we")
tk.Button(tab2, text="Update", command=update_item, bg="AntiqueWhite2", relief="flat",font="Arial 10").grid(row=4, column=4, pady=5, sticky="we")
 
# img = tk.PhotoImage(file=r'C:\Users\Deign\Pictures\Screenshots\avatar.png')
# img1 = img.subsample(4, 6)
# tk.Label(tab2, image=img1, bg="AntiqueWhite2").grid(row=0, column=2, rowspan=3, padx=10, sticky="nsew")

tree = ttk.Treeview(tab2, columns=("Item", "Quantity", "Price"), show="headings")
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", foreground="black", background="pink3")
tree.grid(row=7, column=0, columnspan=5, sticky="nsew")

# Configure column and row weights to make widgets stretchable
tab2.grid_columnconfigure(0, weight=1)
tab2.grid_columnconfigure(1, weight=2)
tab2.grid_columnconfigure(2, weight=1)
tab2.grid_columnconfigure(3, weight=1)
tab2.grid_columnconfigure(4, weight=1)
tab2.grid_rowconfigure(7, weight=1)


for col in ("Item", "Quantity", "Price"):
    tree.heading(col, text=col)
tree.grid(row=7, column=0, columnspan=5)


def search(event):
    query = entry.get().lower()
    tree.delete(*tree.get_children())  

    for row_index, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        if query in str(row[0]).lower(): 
            tree.insert("", "end", values=row, iid=str(row_index))

label = tk.Label(tab2, text="Search", bg="AntiqueWhite2", font="Times 11")
label.grid(row=6, column=0, pady=10, sticky="w")
entry = tk.Entry(tab2, font="Times 11", justify="left")
entry.grid(row=6, column=1, columnspan=4, pady=5, sticky="we")
entry.bind("<KeyRelease>", search)

tab2.grid_columnconfigure(1, weight=1)  
view_data()


def update_total():
    total = 0
    for row_index, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        if row[1] is not None and row[2] is not None:  
            try:
                quantity = float(row[1])
                price = float(row[2])
                total += quantity * price
            except ValueError:
                continue

    total_row = ["Total", "", f"{total:.2f}"]

    for row_index, row in enumerate(ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True), start=2):
        if row[0] == "Total":
            ws.delete_rows(row_index)
            break

    ws.append(total_row)
    wb.save("inventory.xlsx")

    
    tree.delete(*tree.get_children())
    for row_index, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        tree.insert("", "end", values=row, iid=str(row_index))

    
    view_data()


# Tab 3 - History

label2 = tk.Label(tab3, text="History", bg="AntiqueWhite2", font="Arial 14 bold")
label2.grid(row=0, column=0, padx=10, pady=10)

history_tree = ttk.Treeview(tab3, columns=("Action", "Item", "Quantity", "Price", "Timestamp"), show="headings")
history_tree.grid(row=1, column=0, columnspan=5, sticky="nsew")

for col in ("Action", "Item", "Quantity", "Price", "Timestamp"):
    history_tree.heading(col, text=col)

tab3.grid_columnconfigure(0, weight=1)
tab3.grid_rowconfigure(1, weight=1)

# Create a new worksheet for history if it doesn't exist
if "History" not in wb.sheetnames:
    history_ws = wb.create_sheet("History")
    history_ws.append(["Action", "Item", "Quantity", "Price", "Timestamp"])
else:
    history_ws = wb["History"]

def log_action(action, item, quantity, price):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history_ws.append([action, item, quantity, price, timestamp])
    wb.save("inventory.xlsx")
    history_tree.insert("", "end", values=(action, item, quantity, price, timestamp))
    messagebox.showinfo("Action Logged", f"{action} action performed on item '{item}'.")

# Update existing functions to log actions
def add_item_with_logging():
    item, quantity, price = entry_item.get(), entry_quantity.get(), entry_price.get()
    add_item()  # add_item function
    if item and quantity and price:
        log_action("Add", item, quantity, price)

def delete_item_with_logging():
    global selected_item_index
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0], "values")
        delete_item()  # delete_item function
        log_action("Delete", values[0], values[1], values[2])

def update_item_with_logging():
    global selected_item_index
    if selected_item_index:
        new_values = (entry_item.get(), entry_quantity.get(), entry_price.get())
        update_item()  # update_item function
        if all(new_values):
            log_action("Update", new_values[0], new_values[1], new_values[2])

# Replace the button commands to connect in new function 
tk.Button(tab2, text="Add", command=add_item_with_logging, bg="AntiqueWhite2", relief="flat", font="Arial 10").grid(row=4, column=0, pady=5, sticky="we")
tk.Button(tab2, text="Delete", command=delete_item_with_logging, bg="AntiqueWhite2", relief="flat", font="Arial 10").grid(row=4, column=3, pady=5, sticky="we")
tk.Button(tab2, text="Update", command=update_item_with_logging, bg="AntiqueWhite2", relief="flat", font="Arial 10").grid(row=4, column=4, pady=5, sticky="we")

# Load history data into the history_tree
for row in history_ws.iter_rows(min_row=2, values_only=True):
    history_tree.insert("", "end", values=row)

view_data()
update_total()




window.mainloop()
