import tkinter as tk
from tkinter import ttk, messagebox
from operations import get_financial_year, search_flats, get_total_charges, get_total_paid, add_charge, get_charges, add_payment, get_payments
from tkcalendar import DateEntry
from datetime import datetime
from datetime import date

root = tk.Tk()
root.configure(bg="#872B5B")

def search():
    flat_no = flat_entry.get()
    result = search_flats(flat_no)

    if flat_no == "":
        messagebox.showerror("Error", "Enter a flat number")
        return
    
    owner_entry.config(state="normal")
    owner_entry.delete(0, tk.END)

    if result:
        owner_entry.insert(0, result[1])
    else:
        messagebox.showerror("Error", "Flat number not found")
    
    owner_entry.config(state="readonly")

def load_year(event):
    flat_no = flat_entry.get()

    if flat_no == "":
        return
    
    financial_year = year_entry.get()

    total = get_total_charges(flat_no, financial_year)
    paid = get_total_paid(flat_no, financial_year)

    outstanding = total - paid

    total_amount_entry.config(state="normal")
    total_amount_entry.delete(0, tk.END)
    total_amount_entry.insert(0, total)
    total_amount_entry.config(state="readonly")

    pending_amount_entry.config(state="normal")
    pending_amount_entry.delete(0, tk.END)
    pending_amount_entry.insert(0, outstanding)
    pending_amount_entry.config(state="readonly")

    load_charges()

    load_payments()

def add_charge_gui():
    flat_no = flat_entry.get()

    financial_year = year_entry.get()

    amount = amount_entry.get()

    quarter = quarter_entry.get()

    if flat_no == "" or financial_year == "" or amount == "" or quarter == "":
        messagebox.showerror("Error", "Please fill all details")
        return 
    
    if quarter== "Miscellaneous":
        selected_date = misc_date_entry.get()
        from_date = selected_date
        to_date = selected_date
        charge_type = "Miscellaneous" 
    else:
        from_date, to_date, charge_type = get_quarter_details(financial_year, quarter)
    add_charge(flat_no, financial_year, from_date, to_date, amount, charge_type)

    messagebox.showinfo("Success", "Charge added successfully")

    load_charges() 

    total = get_total_charges(flat_no, financial_year)
    paid = get_total_paid(flat_no, financial_year)

    pending = total - paid
    
    total_amount_entry.config(state="normal")
    total_amount_entry.delete(0, tk.END)
    total_amount_entry.insert(0, total)
    total_amount_entry.config(state="readonly")

    pending_amount_entry.config(state="normal")
    pending_amount_entry.delete(0, tk.END)
    pending_amount_entry.insert(0, pending)
    pending_amount_entry.config(state="readonly")

    amount_entry.delete(0, tk.END)
    quarter_entry.set("")

def get_quarter_details(financial_year, quarter):
    start_year = financial_year[:4]
    end_year = str(int(start_year) + 1)

    if quarter == "Q1":
        return f"{start_year}-04-01", f"{start_year}-06-30", "O&M"
    
    if quarter == "Q2":
        return f"{start_year}-07-01", f"{start_year}-09-30", "O&M"
    
    if quarter == "Q3":
        return f"{start_year}-10-01", f"{start_year}-12-31", "O&M"
    
    if quarter == "Q4":
        return f"{end_year}-01-01", f"{end_year}-03-31", "O&M"
    
def load_charges():
    flat_no = flat_entry.get()
    financial_year = year_entry.get()
    records = get_charges(flat_no, financial_year)

    for item in tree.get_children():
        tree.delete(item)
    
    for record in records:

     from_date = datetime.strptime(
        str(record[1]),
        "%Y-%m-%d"
     ).strftime("%d-%b-%Y")

     to_date = datetime.strptime(
        str(record[2]),
        "%Y-%m-%d"
     ).strftime("%d-%b-%Y")

     tree.insert(
        "",
        tk.END,
        values=(
            record[0],
            from_date,
            to_date,
            record[3],
            record[4]
        )
     )

def load_payments():
    flat_no = flat_entry.get()
    financial_year = year_entry.get()

    records = get_payments(flat_no, financial_year)

    for item in payment_tree.get_children():
        payment_tree.delete(item)
    
    for record in records:

     payment_date = datetime.strptime(
        str(record[1]),
        "%Y-%m-%d"
     ).strftime("%d-%b-%Y")

     payment_tree.insert(
        "",
        tk.END,
        values=(
            record[0],
            payment_date,
            record[2]
        )
     )

def add_payement_gui():
    flat_no = flat_entry.get()

    financial_year = year_entry.get()

    payment_date = payment_date_entry.get()

    amount_paid = amount_paid_entry.get()

    if flat_no == "" or financial_year == "" or payment_date == "" or amount_paid == "":
        messagebox.showerror("Error", "Please fill all details")
        return
    
    try:
        amount_paid = float(amount_paid)

        if amount_paid<=0:
            messagebox.showerror("Error", "Amount paid must be greater than 0")
            return
        
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount")
        return
    
    pending = float(pending_amount_entry.get())

    if amount_paid>pending:
        messagebox.showerror("Error", "Amount Paid cannot exceed pending amount")
        return 
    
    add_payment(flat_no, financial_year, payment_date, amount_paid)

    messagebox.showinfo("Success", "Payment added successfully")

    load_payments()

    total = get_total_charges(flat_no, financial_year)

    paid = get_total_paid(flat_no, financial_year)

    pending = total - paid

    total_amount_entry.config(state="normal")
    total_amount_entry.delete(0, tk.END)
    total_amount_entry.insert(0, total)
    total_amount_entry.config(state="readonly")

    pending_amount_entry.config(state="normal")
    pending_amount_entry.delete(0, tk.END)
    pending_amount_entry.insert(0, pending)
    pending_amount_entry.config(state="readonly")

    payment_date_entry.delete(0, tk.END)
    amount_paid_entry.delete(0, tk.END)  

    payment_date_entry.set_date(date.today())

def quarter_changed(event):

    if quarter_entry.get() == "Miscellaneous":
        misc_date_label.grid()
        misc_date_entry.grid()

    else:
        misc_date_label.grid_remove()
        misc_date_entry.grid_remove()
    
    load_charges()

root.title("O & M Charges Management")
root.geometry("1300x700")
root.resizable(True, True)

heading = tk.Label(root, text= "O & M Charges Management", font=("Arial", 18, "bold"))
heading.grid(row = 0, column = 0, columnspan=4, pady=20)

flat_label = tk.Label(root, text="Flat No", font=("Arial", 12))
flat_label.grid(row=1, column=0, padx=15, pady=10, sticky='w')

owner_label = tk.Label(root, text="Owner", font=("Arial", 12))
owner_label.grid(row=2, column=0, padx=15, pady=10, sticky='w')

year_label = tk.Label(root, text="Year", font=("Arial", 12))
year_label.grid(row=3, column=0, padx=15, pady=10, sticky='w')

total_amount_label = tk.Label(root, text="Total Amount", font=("Arial", 12))
total_amount_label.grid(row=1, column=3, padx=15, pady=10, sticky='w')

pending_amount_label = tk.Label(root, text="Pending Amount", font=("Arial", 12))
pending_amount_label.grid(row=2, column=3, padx=15, pady=10, sticky='w')

quarter_label = tk.Label(root, text="Quarter", font=("Arial", 12))
quarter_label.grid(row=4, column=0, padx=15, pady=20, sticky='w')

amount_label = tk.Label(root, text="Amount", font=("Arial", 12))
amount_label.grid(row=5, column=0, padx=15, pady=20, sticky='w')

payment_date_label = tk.Label(root, text="Payment Date", font=("Arial", 12))
payment_date_label.grid(row=3, column=6, padx=15, pady=20, sticky='w')

amount_paid_label = tk.Label(root, text="Amount Paid", font=("Arial", 12))
amount_paid_label.grid(row=4, column=6, padx=15, pady=20, sticky='w')

misc_date_label = tk.Label(root, text="Misc Date", font=("Arial", 12))
misc_date_label.grid(row=6, column=6, padx=15, pady=10, sticky="w")

flat_entry = tk.Entry(root, width= 20)
flat_entry.grid(row=1, column=1, pady=20)
flat_entry.bind("<Return>", lambda event: search())

owner_entry = tk.Entry(root, width=20)
owner_entry.grid(row=2, column=1, pady=20)

year_entry = ttk.Combobox(root, width=20, state="readonly")
year_entry.grid(row=3, column=1, pady=15)
year_entry.bind("<<ComboboxSelected>>", load_year)

years = [year[0] for year in get_financial_year()]
year_entry["values"] = years

total_amount_entry = tk.Entry(root, width=20)
total_amount_entry.grid(row=1, column=6, pady=20)

pending_amount_entry = tk.Entry(root, width=20)
pending_amount_entry.grid(row=2, column=6, pady=20)

quarter_entry = ttk.Combobox(root, width=18, state="readonly")
quarter_entry["values"] = ("Q1", "Q2", "Q3", "Q4", "Miscellaneous")
quarter_entry.grid(row=4, column=1, pady=10)
quarter_entry.bind("<<ComboboxSelected>>", quarter_changed)

amount_entry = tk.Entry(root, width=20)
amount_entry.grid(row=5, column=1, pady=15)

payment_date_entry = DateEntry(root, width=20, date_pattern = "yyyy-mm-dd")
payment_date_entry.grid(row=3, column=7, pady=15)

misc_date_entry= DateEntry(root, width=18, date_pattern="yyyy-mm-dd")
misc_date_entry.grid(row=6, column=7, pady=10)

misc_date_label.grid_remove()
misc_date_entry.grid_remove()

amount_paid_entry = tk.Entry(root, width=20)
amount_paid_entry.grid(row=4, column=7, pady=15)

table_frame = tk.Frame(root)
table_frame.grid(row=7, column=0, columnspan=4, padx=20, pady=(5,15))

payment_frame = tk.Frame(root)
payment_frame.grid(row=7, column=4, columnspan=4, padx=20, pady=(5,15), sticky='n')

add_button = tk.Button(root, text="Add Charge", command=add_charge_gui)
add_button.grid(row=5, column=3, padx=15, pady=20)
tree = ttk.Treeview(table_frame, height = 8)

add_payment_button = tk.Button(root, text="Add Payment", command=add_payement_gui)
add_payment_button.grid(row=5, column=7, pady=20)

charges_label = tk.Label(root, text="Charges", font=("Arial", 12, "bold"))
charges_label.grid(row=6, column=0, columnspan=2, pady=(10, 5))

tree["columns"] = ["S.No", "From Date", "To Date", "Amount", "Type"]

tree.column("#0", width=0, stretch=False)

tree.column("S.No", width=55, anchor="center")
tree.column("From Date", width=110, anchor="center")
tree.column("To Date", width=110, anchor="center")
tree.column("Amount", width=120, anchor="center")
tree.column("Type", width=90, anchor="center")

tree.heading("#0", text="")

tree.heading("S.No", text="S.No")
tree.heading("From Date", text="From Date")
tree.heading("To Date", text="To Date")
tree.heading("Amount", text="Quarter Amount")
tree.heading("Type", text="Type")

tree.pack()

payments_label = tk.Label(root, text="Payment History", font=("Arial", 12, "bold"))
payments_label.grid(row=6, column=3, columnspan=2, pady=(10, 5))


payment_tree = ttk.Treeview(payment_frame, height=8)
payment_tree["columns"] = ("ID", "Payment Date", "Amount Paid")

payment_tree.column("#0", width=0, stretch=False)
payment_tree.heading("#0", text="")

payment_tree.column("ID", width=60, anchor="center")
payment_tree.column("Payment Date", width=120, anchor="center")
payment_tree.column("Amount Paid", width=120, anchor="center")

payment_tree.heading("ID", text="ID")
payment_tree.heading("Payment Date", text="Payment Date")
payment_tree.heading("Amount Paid", text="Amount Paid")

payment_tree.pack()

root.mainloop()