from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3

root = Tk()
root.title("Student Book Tracker")
root.geometry("950x450")
root.configure(bg="white")

conn = sqlite3.connect("library.db")

cur = conn.cursor()

def populate_box(combobox):
    cur.execute("SELECT book From books")
    data = [row[0] for row in cur.fetchall()]

    combobox["values"] = data


# --- Search Bar ---
srch_frame = Frame(root, bg="white")
srch_frame.pack(fill=X, padx=10, pady=5)

Label(srch_frame, text="Search:", font=("Segoe UI", 10, "bold"), bg="white").pack(side=LEFT, padx=(0, 5))
srch_entry = Entry(srch_frame, width=40, font=("Segoe UI", 10))
srch_entry.pack(side=LEFT)

Label(srch_frame, text="Total Borrowed Books: 2", font=("Segoe UI", 10, "bold"), bg="white").pack(side=RIGHT)

# --- Left Frame (Form) ---
form_frame = LabelFrame(root, text="Borrow Book", font=("Segoe UI", 11, "bold"), padx=15, pady=10, bg="lightgrey")
form_frame.pack(side=LEFT, padx=10, pady=10, fill=Y)

sn_label = Label(form_frame, text="Student Name:", bg="lightgrey").grid(row=0, column=0, sticky=W, pady=5)
sn_entry = Entry(form_frame, width=25, font=("Segoe UI", 10))
sn_entry.grid(row=0, column=1, pady=5)

bk_entry = Label(form_frame, text="Book:", bg="lightgrey").grid(row=1, column=0, sticky=W, pady=5)
bk_entry = ttk.Combobox(form_frame, width=22, font=("Segoe UI", 10))
bk_entry.grid(row=1, column=1, pady=5)

bd_entry = Label(form_frame, text="Borrow Date:", bg="lightgrey").grid(row=2, column=0, sticky=W, pady=5)
bd_entry = DateEntry(form_frame, date_pattern="mm/dd/yy", width=20, font=("Segoe UI", 10))
bd_entry.grid(row=2, column=1, pady=5)

Label(form_frame, text="Return Date:", bg="lightgrey").grid(row=3, column=0, sticky=W, pady=5)
rtd_entry = DateEntry(form_frame, date_pattern="mm/dd/yy", width=20, font=("Segoe UI", 10))
rtd_entry.grid(row=3, column=1, pady=5)

def add_to_borrowed():
    conn = sqlite3.connect("library.db")

    cur = conn.cursor()

    name = sn_entry.get()
    book = bk_entry.get()
    borrow_date = bd_entry.get()
    return_date = rtd_entry.get()

    cur.execute(f"INSERT INTO borrowed_books (student_name, book_id, borrow_date, return_date) VALUES ('{name}', '{book}', '{borrow_date}', '{return_date}')")

    conn.commit()


# --- Buttons ---
btn_frame = Frame(form_frame, bg="lightgrey")
btn_frame.grid(row=4, column=0, columnspan=2, pady=(15, 0))

add = Button(btn_frame, text="Add", bg="green", fg="white", font=("Segoe UI", 9, "bold"), width=8, command=add_to_borrowed)
add.grid(row=0, column=0, padx=5)

delete = Button(btn_frame, text="Delete", bg="red", fg="white", font=("Segoe UI", 9, "bold"), width=8)
delete.grid(row=0, column=1, padx=5)

clear = Button(btn_frame, text="Clear", bg="grey", fg="black", font=("Segoe UI", 9, "bold"), width=8)
clear.grid(row=0, column=2, padx=5)

# --- Right Frame (Table) ---
table_frame = Frame(root)
table_frame.pack(side=RIGHT, padx=10, pady=10, fill=BOTH, expand=True)

tree = ttk.Treeview(table_frame, columns=("ID", "Student", "Book", "Borrow Date", "Return Date", "Fine"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Student", text="Student")
tree.heading("Book", text="Book")
tree.heading("Borrow Date", text="Borrow Date")
tree.heading("Return Date", text="Return Date")
tree.heading("Fine", text="Fine")

tree.column("ID", width=40, anchor=CENTER)
tree.column("Student", width=120)
tree.column("Book", width=150)
tree.column("Borrow Date", width=100, anchor=CENTER)
tree.column("Return Date", width=100, anchor=CENTER)
tree.column("Fine", width=60, anchor=CENTER)

tree.pack(fill=BOTH, expand=True)

# --- Scrollbar ---
scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)


populate_box(bk_entry)


# --- Load Data ---
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
