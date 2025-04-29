import tkinter as tk
from tkinter import ttk
from openpyxl import load_workbook, Workbook




try:
    wb = load_workbook("inventory.xlsx")
except FileNotFoundError:
    wb = Workbook()
    ws = wb.active
    ws.append(["Item", "Quantity", "Price"])  
    wb.save("inventory.xlsx")

ws = wb.active
selected_item_index = None 

def add_item():
    item, quantity, price = entry_item.get(), entry_quantity.get(), entry_price.get()
    if item and quantity and price:
        ws.append([item, quantity, price])
        wb.save("inventory.xlsx")
        tree.insert("", "end", values=(item, quantity, price))
        clear_entries()

def view_data():
    tree.delete(*tree.get_children())
    for row_index, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        tree.insert("", "end", values=row, iid=str(row_index))  # Assign row index as ID

def delete_item():
    global selected_item_index
    selected = tree.selection()
    if selected:
        row_index = int(selected[0])  # Get row index
        ws.delete_rows(row_index)  # Remove correct row
        wb.save("inventory.xlsx")
        tree.delete(selected[0])  # Remove from UI
        selected_item_index = None  # Reset after deletion

def edit_item():
    global selected_item_index
    selected = tree.selection()
    if selected:
        selected_item_index = int(selected[0])  # Store row index
        values = tree.item(selected[0], "values")
        entry_item.delete(0, tk.END)
        entry_item.insert(0, values[0])
        entry_quantity.delete(0, tk.END)
        entry_quantity.insert(0, values[1])
        entry_price.delete(0, tk.END)
        entry_price.insert(0, values[2])

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

def clear_entries():
    entry_item.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_price.delete(0, tk.END)

# GUI Setup
window = tk.Tk()
window.title("Inventory Management")
window.configure(bg="AntiqueWhite2")

tk.Label(window, text="Item", bg="AntiqueWhite2", font="Times 11").grid(row=0, column=0)
tk.Label(window, text="Quantity", bg="AntiqueWhite2", font="Times 11").grid(row=1, column=0)
tk.Label(window, text="Price", bg="AntiqueWhite2", font="Times 11").grid(row=2, column=0)


entry_item, entry_quantity, entry_price = tk.Entry(window, font="Times 11", justify="right"), tk.Entry(window, font="Times 11 ", justify="right"), tk.Entry(window, font="Times 11", justify="right")

entry_item.grid(row=0, column=1, pady=5)
entry_quantity.grid(row=1, column=1, pady=5)
entry_price.grid(row=2, column=1, pady=5)

tk.Button(window, text="Add", command=add_item).grid(row=4, column=0, pady=5)
tk.Button(window, text="Refresh", command=view_data).grid(row=4, column=1, pady=5)
tk.Button(window, text="Edit", command=edit_item).grid(row=4, column=2, pady=5)
tk.Button(window, text="Delete", command=delete_item).grid(row=4, column=3, pady=5)
tk.Button(window, text="Update", command=update_item).grid(row=4, column=4, pady=5)

img = tk.PhotoImage(file = r'C:\Users\Deign\Pictures\Screenshots\avatar.png')
img1 = img.subsample(3, 3)
tk.Label(window, image=img1, bg="AntiqueWhite2").grid(row=0, column=2, rowspan=3, padx=10)


tree = ttk.Treeview(window, columns=("Item", "Quantity", "Price"), show="headings")
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", foreground="black", background="pink3")


for col in ("Item", "Quantity", "Price"):
    tree.heading(col, text=col)
tree.grid(row=5, column=0, columnspan=5)

view_data()

window.mainloop()