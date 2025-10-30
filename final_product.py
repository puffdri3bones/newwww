from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
from datetime import date

# Part 1 - Database Setup
def setup_database():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()

    # Create tables
    cur.execute("""CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS borrowed_books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT NOT NULL,
        book_id INTEGER,
        borrow_date TEXT,
        return_date TEXT,
        fine REAL DEFAULT 0,
        FOREIGN KEY(book_id) REFERENCES books(id)
    )""")

    # Insert sample data if empty
    cur.execute("SELECT COUNT(*) FROM books")
    if cur.fetchone()[0] == 0:
        sample_books = [
            ("Learn Python", 5),
            ("Database Systems", 4),
            ("Web Development", 3),
            ("AI Fundamentals", 2),
            ("Networking Basics", 1),
        ]
        cur.executemany("INSERT INTO books (title, quantity) VALUES (?,?)", sample_books)

    cur.execute("SELECT COUNT(*) FROM borrowed_books")
    if cur.fetchone()[0] == 0:
        sample_borrowed = [
            ("Alice Johnson", 1, "06/01/25", "06/10/25", 0),
            ("Bob Smith", 2, "06/05/25", "06/12/25", 0)
        ]
        cur.executemany(
            "INSERT INTO borrowed_books (student_name, book_id, borrow_date, return_date, fine) VALUES (?,?,?,?,?)",
            sample_borrowed
        )

    conn.commit()
    conn.close()

setup_database()

# MAIN WINDOW
root = Tk()
root.title("Student Book Tracker")
root.geometry("950x450")
root.configure(bg="white")

# DB CONNECTION
def connect_db():
    return sqlite3.connect("library.db")

# POPULATE BOOK DROPDOWN 
def populate_books():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT title FROM books WHERE quantity > 0")
    books = [r[0] for r in cur.fetchall()]
    conn.close()
    book_combo["values"] = books

# CLEAR FORM 
def clear_form():
    student_entry.delete(0, END)
    book_combo.set("")
    borrow_date.set_date(date.today())
    return_date.set_date(date.today())

# REFRESH TABLE 
def refresh_table():
    for item in tree.get_children():
        tree.delete(item)

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""SELECT borrowed_books.id, student_name, books.title, borrow_date, return_date, fine
                   FROM borrowed_books
                   JOIN books ON borrowed_books.book_id = books.id""")
    rows = cur.fetchall()
    conn.close()

    for row in rows:
        tag = "fine" if row[5] > 0 else ""
        tree.insert("", END, values = row, tags=(tag,))
    total_label.config(text=f"Total Borrowed Books: {len(rows)}")

# ADD RECORD
def add_record():
    name = student_entry.get().strip()
    book = book_combo.get()
    b_date = borrow_date.get_date()
    r_date = return_date.get_date()
    today = date.today()

    if not name or not book:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return
    if b_date < today:
        messagebox.showerror("Date Error", "Borrow date cannot be in the past.")
        return
    if r_date < b_date:
        messagebox.showerror("Date Error", "Return date cannot be before borrow date.")
        return

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id, quantity FROM books WHERE title=?", (book,))
    book_data = cur.fetchone()

    if not book_data:
        messagebox.showerror("Error", "Selected book not found.")
        conn.close()
        return

    book_id, qty = book_data
    if qty <= 0:
        messagebox.showinfo("Unavailable", "No copies left for this book.")
        conn.close()
        return

    fine = 0
   
    if r_date > b_date:  # returned late
        overdue_days = r_date - b_date
        days_late = overdue_days.days
        fine = days_late * 5


    print(today)
    print(r_date)

    print(fine)

    cur.execute("""INSERT INTO borrowed_books (student_name, book_id, borrow_date, return_date, fine)
                   VALUES (?,?,?,?,?)""",
                (name, book_id, b_date.strftime("%m/%d/%y"), r_date.strftime("%m/%d/%y"), fine))

    cur.execute("UPDATE books SET quantity = quantity - 1 WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

    populate_books()
    refresh_table()
    clear_form()

# DELETE RECORD
def delete_record():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Record", "Please select a record to delete.")
        return
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
    if not confirm:
        return

    item = tree.item(selected[0])
    borrow_id = item["values"][0]
    book_title = item["values"][2]

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM books WHERE title=?", (book_title,))
    book_id = cur.fetchone()[0]

    cur.execute("DELETE FROM borrowed_books WHERE id=?", (borrow_id,))
    cur.execute("UPDATE books SET quantity = quantity + 1 WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

    populate_books()
    refresh_table()

# SEARCH 
def search_records(event=None):
    query = search_entry.get().lower()
    for item in tree.get_children():
        tree.delete(item)

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""SELECT borrowed_books.id, student_name, books.title, borrow_date, return_date, fine
                   FROM borrowed_books
                   JOIN books ON borrowed_books.book_id = books.id
                   WHERE LOWER(student_name) LIKE ? OR LOWER(books.title) LIKE ?""",
                (f"%{query}%", f"%{query}%"))
    
    rows = cur.fetchall()

    conn.close()

    for row in rows:
        tag = "fine" if row[5] > 0 else ""
        tree.insert("", END, values=row, tags=(tag,))
    total_label.config(text=f"Total Borrowed Books: {len(rows)}")

# SEARCH BAR 
search_frame = Frame(root, bg="white")
search_frame.pack(fill=X, padx=10, pady=5)

Label(search_frame, text="Search:", font=("Segoe UI", 10, "bold"), bg="white").pack(side=LEFT, padx=(0,5))
search_entry = Entry(search_frame, width=40, font=("Segoe UI", 10))
search_entry.pack(side=LEFT)
search_entry.bind("<KeyRelease>", search_records)

total_label = Label(search_frame, text="Total Borrowed Books: 0", font=("Segoe UI", 10, "bold"), bg="white")
total_label.pack(side=RIGHT)

#Part 2 - Borrow Book Form
form_frame = LabelFrame(root, text="Borrow Book", font=("Segoe UI", 11, "bold"),
                        padx=15, pady=10, bg="#f0f0f0", labelanchor="n")
form_frame.pack(side=LEFT, padx=10, pady=10, fill=Y)

Label(form_frame, text="Student Name:", bg="#f0f0f0").grid(row=0, column=0, sticky=W, pady=5)
student_entry = Entry(form_frame, width=25, font=("Segoe UI", 10))
student_entry.grid(row=0, column=1, pady=5)

Label(form_frame, text="Book:", bg="#f0f0f0").grid(row=1, column=0, sticky=W, pady=5)
book_combo = ttk.Combobox(form_frame, width=22, font=("Segoe UI", 10))
book_combo.grid(row=1, column=1, pady=5)

Label(form_frame, text="Borrow Date:", bg="#f0f0f0").grid(row=2, column=0, sticky=W, pady=5)
borrow_date = DateEntry(form_frame, date_pattern="mm/dd/yy", width=20, font=("Segoe UI", 10))
borrow_date.grid(row=2, column=1, pady=5)

Label(form_frame, text="Return Date:", bg="#f0f0f0").grid(row=3, column=0, sticky=W, pady=5)
return_date = DateEntry(form_frame, date_pattern="mm/dd/yy", width=20, font=("Segoe UI", 10))
return_date.grid(row=3, column=1, pady=5)

btn_frame = Frame(form_frame, bg="#f0f0f0")
btn_frame.grid(row=4, column=0, columnspan=2, pady=(15,0))

Button(btn_frame, text="Add", bg="green", fg="white", width=8, font=("Segoe UI", 9, "bold"), command=add_record).grid(row=0, column=0, padx=5)
Button(btn_frame, text="Delete", bg="red", fg="white", width=8, font=("Segoe UI", 9, "bold"), command=delete_record).grid(row=0, column=1, padx=5)
Button(btn_frame, text="Clear", bg="grey", fg="black", width=8, font=("Segoe UI", 9, "bold"), command=clear_form).grid(row=0, column=2, padx=5)

# TABLE 
table_frame = Frame(root)
table_frame.pack(side=RIGHT, padx=10, pady=10, fill=BOTH, expand=True)

tree = ttk.Treeview(table_frame, columns=("ID","Student","Book","Borrow Date","Return Date","Fine"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Student", text="Student")
tree.heading("Book", text="Book")
tree.heading("Borrow Date", text="Borrow Date")
tree.heading("Return Date", text="Return Date")
tree.heading("Fine", text="Fine")

tree.column("ID", width=40, anchor=CENTER)
tree.column("Student", width=150)
tree.column("Book", width=160)
tree.column("Borrow Date", width=100, anchor=CENTER)
tree.column("Return Date", width=100, anchor=CENTER)
tree.column("Fine", width=60, anchor=CENTER)

style = ttk.Style()
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="blue", foreground="white")
style.map("Treeview", background=[("selected", "#a6a6a6")])
tree.tag_configure("fine", background="#ffcccc")

tree.pack(fill=BOTH, expand=True)

scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)

# INITIAL LOAD 
populate_books()
refresh_table()

root.mainloop()
