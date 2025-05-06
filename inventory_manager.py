import tkinter as tk
from tkinter import ttk
from openpyxl import load_workbook, Workbook
from datetime import datetime
from tkinter import messagebox, simpledialog
import os

EXCEL_FILE = 'credentials.xlsx'

def log_login_time(username):
    history_file = "login_history.xlsx"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not os.path.exists(history_file):
        wb = Workbook() 
        ws = wb.active
        ws.append(["Username", "Timestamp"])
        wb.save(history_file)

    wb = load_workbook(history_file)
    ws = wb.active
    ws.append([username, now])
    wb.save(history_file)
    wb.close()

def init_credentials_file():
    if not os.path.exists(EXCEL_FILE):
        wb = Workbook()
        ws = wb.active
        ws.append(["Username", "Password"])
        ws.append(["admin", "admin123"])
        wb.save(EXCEL_FILE)

def validate_login(username, password):
    wb = load_workbook(EXCEL_FILE)
    ws = wb.active
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] == username and row[1] == password:
            wb.close()
            return True
    wb.close()
    return False

def user_exists(username):
    wb = load_workbook(EXCEL_FILE)
    ws = wb.active
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] == username:
            wb.close()
            return True
    wb.close()
    return False

def register():
    user = reg_username.get().strip()
    pwd = reg_password.get().strip()

    if not user or not pwd:
        messagebox.showwarning("Input Error", "Please fill in both fields.")
        return

    if user_exists(user):
        messagebox.showerror("Error", "Username already exists.")
    else:
        register_user(user, pwd)
        messagebox.showinfo("Success", "User registered successfully!")
        show_login_page()

def register_user(username, password):
    wb = load_workbook(EXCEL_FILE)
    ws = wb.active
    ws.append([username, password])
    wb.save(EXCEL_FILE)
    wb.close()

def login():
    global current_user
    user = login_username.get().strip()
    pwd = login_password.get().strip()

    if not user or not pwd:
        messagebox.showwarning("Input Error", "Please fill in both fields.")
        return

    if validate_login(user, pwd):
        current_user = user
        log_login_time(user)
        messagebox.showinfo("Login Success", f"Welcome, {user}!")
        inventoryWindow()
    else:
        messagebox.showerror("Login Failed", "Invalid credentials.")

def show_login_page():
    if 'register_frame' in globals() and 'login_frame' in globals():
        register_frame.grid_forget()
        login_frame.grid()
    else:
        messagebox.showerror("Error", "Frames are not initialized.")


def show_register_page():
    if 'login_frame' in globals() and 'register_frame' in globals():
        login_frame.grid_forget()
        register_frame.grid()
    else:
        messagebox.showerror("Error", "Frames are not initialized.")

def inventoryWindow():
    root.withdraw()
    PASSWORD = "admin123"
    def on_tab_changed(event):
        selected_tab = event.widget.index("current")
    
    # If user selects the protected tab (index 1)
        if selected_tab == 4 and not access_granted[0]:
            pwd = simpledialog.askstring("Password Required", "Enter password:", show="*")
            if pwd == PASSWORD:
                access_granted[0] = True
            else:
                messagebox.showerror("Access Denied", "Incorrect password.")
                notebook.select(0)  # Revert to first tab

    access_granted = [False]
    
    Management = tk.Toplevel(root)
    Management.title("Inventory Management")
    Management.configure(bg="AntiqueWhite2")

    style = ttk.Style()
    style.configure('lefttab.TNotebook', tabposition='ws', relief="flat")  # Set tabs to the left side
    notebook = ttk.Notebook(Management, style='lefttab.TNotebook')

    # Add a second notebook for bottom tabs
    bottom_style = ttk.Style()
    bottom_style.configure('bottomtab.TNotebook', tabposition='s', relief="flat")  # Set tabs to the bottom
    bottom_notebook = ttk.Notebook(Management, style='bottomtab.TNotebook')

    tab1 = tk.Frame(notebook, bg="AntiqueWhite2")
    tab2 = tk.Frame(notebook, bg="AntiqueWhite2")
    tab3 = tk.Frame(notebook, bg="AntiqueWhite2")
    tab4 = tk.Frame(notebook, bg="AntiqueWhite2")
    tab5 = tk.Frame(notebook, bg="AntiqueWhite2")
   

    

    style.theme_use("clam")

    style.configure("TNotebook", background="RosyBrown3")  
    style.configure("TNotebook.Tab", background="RosyBrown3", foreground="black")
    style.map("TNotebook.Tab", background=[("selected", "AntiqueWhite2")], foreground=[("selected", "black")])

    notebook.grid(sticky="nsew")
    style.configure('lefttab.TNotebook', tabposition='wn')  # Set tabs to the left side
    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

    # Make the notebook stretchable
    Management.grid_columnconfigure(0, weight=1)
    Management.grid_rowconfigure(0, weight=1)

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
            tree.insert("", "end", values=row, iid=str(row_index))  
    def delete_item():
        global selected_item_index
        selected = tree.selection()
        if selected:
            row_index = int(selected[0])  #row index
            ws.delete_rows(row_index)  
            wb.save("inventory.xlsx")
            tree.delete(selected[0])  
            selected_item_index = None  # Reset after deletion
            update_total()  # Update total after deleting an item
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
                update_total()  # Update total after updating an item
                clear_entries()
                selected_item_index = None

    def clear_entries():
        entry_item.delete(0, tk.END)
        entry_quantity.delete(0, tk.END)
        entry_price.delete(0, tk.END)

    def logout():
        if Management.winfo_exists():  # Check if the window exists
            Management.destroy()
        root.deiconify()
    Management.protocol("WM_DELETE_WINDOW", logout)

    label1 = tk.Label(tab1, text="Inventory Management", bg="AntiqueWhite2", font="Arial 14 bold")
    label1.grid(row=0, column=0, padx=10, pady=10)

    tk.Button(tab1, text="Logout",command=logout, font="Arial 10").grid(row=0, column=5, pady=5, sticky="w")

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

    tree = ttk.Treeview(tab2, columns=("Item", "Quantity", "Price"), show="headings")
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", foreground="black", background="pink3")
    tree.grid(row=7, column=0, columnspan=5, sticky="nsew")

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

    label2 = tk.Label(tab3, text="History", bg="AntiqueWhite2", font="Arial 14 bold", justify="center")
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

    def add_item_with_logging():
        item, quantity, price = entry_item.get(), entry_quantity.get(), entry_price.get()
        add_item()  # Call the original add_item function
        if item and quantity and price:
            log_action("Add", item, quantity, price)

    def delete_item_with_logging():
        global selected_item_index
        selected = tree.selection()
        if selected:
            values = tree.item(selected[0], "values")
            delete_item()  # Call the original delete_item function
            log_action("Delete", values[0], values[1], values[2])

    def update_item_with_logging():
        global selected_item_index
        if selected_item_index:
            new_values = (entry_item.get(), entry_quantity.get(), entry_price.get())
            update_item()  # Call the original update_item function
            if all(new_values):
                log_action("Update", new_values[0], new_values[1], new_values[2])
    
    tk.Button(tab2, text="Add", command=add_item_with_logging, bg="AntiqueWhite2", relief="flat", font="Arial 10").grid(row=4, column=0, pady=5, sticky="we")
    tk.Button(tab2, text="Delete", command=delete_item_with_logging, bg="AntiqueWhite2", relief="flat", font="Arial 10").grid(row=4, column=3, pady=5, sticky="we")
    tk.Button(tab2, text="Update", command=update_item_with_logging, bg="AntiqueWhite2", relief="flat", font="Arial 10").grid(row=4, column=4, pady=5, sticky="we")

    for row in history_ws.iter_rows(min_row=2, values_only=True):
        history_tree.insert("", "end", values=row)
    
    def search_history(event):
        query = history_entry.get().lower()
        history_tree.delete(*history_tree.get_children())  

        for row_index, row in enumerate(history_ws.iter_rows(min_row=2, values_only=True), start=2):
            if query in " ".join(map(str, row)).lower(): 
                history_tree.insert("", "end", values=row, iid=str(row_index))

    history_label = tk.Label(tab3, text="Search History", bg="AntiqueWhite2", font="Times 11")
    history_label.grid(row=2, column=0, pady=10, sticky="w")
    history_entry = tk.Entry(tab3, font="Times 11", justify="left")
    history_entry.grid(row=2, column=1, columnspan=4, pady=5, sticky="we")
    history_entry.bind("<KeyRelease>", search_history)

    tab3.grid_columnconfigure(1, weight=1)

    view_data()
    update_total()
    
init_credentials_file()

root = tk.Tk()
root.title("Login & Admin Management")

root.configure(bg="AntiqueWhite2")
root.resizable(False, False)

# ---------------------- Login Frame ---------------------
login_frame = tk.Frame(root, bg="AntiqueWhite2")
login_frame.grid(row=0, column=0, sticky="nsew")

tk.Label(login_frame, text="Login", font=("Arial", 14), bg="AntiqueWhite2").grid(row=0, column=0, columnspan=2, pady=10)
tk.Label(login_frame, text="Username", bg="AntiqueWhite2").grid(row=1, column=0, padx=10, pady=5, sticky="e")
login_username = tk.Entry(login_frame)
login_username.grid(row=1, column=1, padx=10, pady=5, sticky="w")
tk.Label(login_frame, text="Password", bg="AntiqueWhite2").grid(row=2, column=0, padx=10, pady=5, sticky="e")
login_password = tk.Entry(login_frame, show='*')
login_password.grid(row=2, column=1, padx=10, pady=5, sticky="w")
tk.Button(login_frame, text="Login", command=login).grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(login_frame, text="Register", command=show_register_page).grid(row=4, column=0, columnspan=2)

# ---------------------- Register Frame ---------------------
register_frame = tk.Frame(root, bg="AntiqueWhite2")
register_frame.grid(row=0, column=0, sticky="nsew")

tk.Label(register_frame, text="Register", font=("Arial", 14), bg="AntiqueWhite2").grid(row=0, column=0, columnspan=2, pady=10)
tk.Label(register_frame, text="Username", bg="AntiqueWhite2").grid(row=1, column=0, padx=10, pady=5, sticky="e")
reg_username = tk.Entry(register_frame)
reg_username.grid(row=1, column=1, padx=10, pady=5, sticky="w")
tk.Label(register_frame, text="Password", bg="AntiqueWhite2").grid(row=2, column=0, padx=10, pady=5, sticky="e")
reg_password = tk.Entry(register_frame, show='*')
reg_password.grid(row=2, column=1, padx=10, pady=5, sticky="w")
tk.Button(register_frame, text="Submit", command=register).grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(register_frame, text="Back to Login", command=show_login_page).grid(row=4, column=0, columnspan=2)

root.mainloop()