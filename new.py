from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3

root = Tk()
root.title("Student Book Tracker")
root.geometry("950x450")

# --- Top Bar ---
Label(root, text="Borrow Book", font=("Arial", 11, "bold")).place(x=20, y=10)

Label(root, text="Search:").place(x=550, y=10)
srch_entry = Entry(root, width=30)
srch_entry.place(x=600, y=10)

Label(root, text="Total Borrowed Books: 2", font=("Arial", 10, "bold")).place(x=780, y=10)

# --- Left Section (Borrow Book Box) ---
fieldset = ttk.Frame(root, borderwidth=3, relief="groove")
fieldset.place(x=20, y=40, width=380, height=350)

# Inside the fieldset
Label(fieldset, text="Student Name:").grid(row=0, column=0, sticky=W, padx=10, pady=(20, 5))
sn_entry = Entry(fieldset, width=25)
sn_entry.grid(row=0, column=1, pady=(20, 5))

Label(fieldset, text="Book:").grid(row=1, column=0, sticky=W, padx=10, pady=5)
bk_entry = ttk.Combobox(fieldset, width=22)
bk_entry.grid(row=1, column=1, pady=5)

Label(fieldset, text="Borrow Date:").grid(row=2, column=0, sticky=W, padx=10, pady=5)
bd_entry = DateEntry(fieldset, date_pattern="mm/dd/yy", width=18)
bd_entry.grid(row=2, column=1, pady=5)

Label(fieldset, text="Return Date:").grid(row=3, column=0, sticky=W, padx=10, pady=5)
rtd_entry = DateEntry(fieldset, date_pattern="mm/dd/yy", width=18)
rtd_entry.grid(row=3, column=1, pady=5)

# Buttons
add = Button(fieldset, text="Add", bg="green", fg="white", width=5)
add.grid(row=4, column=0, pady=(25, 5))

delete = Button(fieldset, text="Delete", bg="red", fg="white", width=5)
delete.grid(row=4, column=1, pady=(25, 5))

clear = Button(fieldset, text="Clear", bg="grey", fg="black", width=5)
clear.grid(row=4, column=2, pady=(25, 5))

# --- Right Section (Table) ---
table_frame = ttk.Frame(root, borderwidth=2, relief="groove")
table_frame.place(x=570, y=40, width=380, height=350)

tree = ttk.Treeview(table_frame, columns=("c1", "c2", "c3", "c4", "c5", "c6"), show="headings")
tree.heading("c1", text="ID")
tree.heading("c2", text="Student")
tree.heading("c3", text="Book")
tree.heading("c4", text="Borrow Date")
tree.heading("c5", text="Return Date")
tree.heading("c6", text="Fine")

tree.column("c1", width=40, anchor=CENTER)
tree.column("c2", width=120)
tree.column("c3", width=140)
tree.column("c4", width=100, anchor=CENTER)
tree.column("c5", width=100, anchor=CENTER)
tree.column("c6", width=50, anchor=CENTER)

# Scrollbar
scrollbar = Scrollbar(table_frame, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
tree.pack(fill=BOTH, expand=True)

# --- Database View Function ---
def view():
    con1 = sqlite3.connect("library.db")
    cur1 = con1.cursor()
    cur1.execute("SELECT * FROM borrowed_books")
    rows = cur1.fetchall()
    for row in rows:
        tree.insert("", END, values=row)
    con1.close()

view()

root.mainloop()
