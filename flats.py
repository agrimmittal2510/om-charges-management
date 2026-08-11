import tkinter as tk
from operations import search_flats, get_all_flats
from tkinter import ttk, messagebox

def load_flats():
    records = get_all_flats()

    for item in tree.get_children():
        tree.delete(item)
    
    for record in records:
        tree.insert("", tk.END, values = record)

def search():

    flat_no = flat_entry.get()

    if flat_no == "":
        messagebox.showerror("Error", "Enter Flat Number")
        return

    result = search_flats(flat_no)

    owner_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)

    if result:
        owner_entry.insert(0, result[1])
        phone_entry.insert(0, result[2])
    else:
        messagebox.showerror("Error", "Flat not found")

def clear_all():
    flat_entry.delete(0, tk.END)
    owner_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)

    for item in tree.get_children():
        tree.delete(item)
    
    flat_entry.focus_set()


root = tk.Tk()

root.title("Flats Detail")
root.geometry("700x500")

heading = tk.Label(root, text="Flats Details", font=("Arial", 18, "bold"))

heading.grid(row=0, column=0, columnspan=3, pady=20)

flat_label = tk.Label(root, text="Flat No")
flat_label.grid(row=1, column=0, padx=20, pady=20, sticky='w')

flat_entry = tk.Entry(root, width=20)
flat_entry.grid(row=1, column=1)

owner_label = tk.Label(root,text="Owner")
owner_label.grid(row=2,column=0,padx=10,pady=10,sticky="w")

owner_entry = tk.Entry(root,width=30)
owner_entry.grid(row=2,column=1)

phone_label = tk.Label(root,text="Phone Number")
phone_label.grid(row=3,column=0,padx=10,pady=10,sticky="w")

phone_entry = tk.Entry(root,width=30)
phone_entry.grid(row=3,column=1)

search_button = tk.Button(root, text="Search", command=search)

search_button.grid(row=1,column=2,padx=10)

view_button = tk.Button(root, text="View All Flats")
view_button.config(command=load_flats)

view_button.grid(row=4,column=1,pady=15)

clear_button = tk.Button(root, text="Clear", command=clear_all)
clear_button.grid(row=1, column=3, padx=10)

tree = ttk.Treeview(root)

tree["columns"] = ("Flat","Owner","Phone")

tree.column("#0",width=0,stretch=False)

tree.column("Flat",width=100,anchor="center")
tree.column("Owner",width=180,anchor="center")
tree.column("Phone",width=150,anchor="center")

tree.heading("#0",text="")

tree.heading("Flat",text="Flat No")
tree.heading("Owner",text="Owner")
tree.heading("Phone",text="Phone Number")

tree.grid(row=5,column=0,columnspan=3,padx=20,pady=20)

root.mainloop()
