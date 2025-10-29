from tkinter import * 
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3

def add_to_books():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()

    book_id = input("Enter book ID number: ")
    book_name = input("Enter book name: ")
    quantity = input("Enter book quantity: ")
    cur.execute(f"""INSERT INTO books (id, book, quantity) VALUES ("{book_id}","{book_name}","{quantity}")""") 
    conn.commit()
    conn.close()
       
        
add_to_books()

def add_to_borrowed():
    
    bkname = bk_entry.get()
    bk_entry["values"] = bkname 
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute(f"""INSERT INTO borrowed_books (id, book, quantity) VALUES (3,"{bkname}", 6)""")
    conn.commit()
    conn.close()

def del_from_db():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()
    cur.execute("""DELETE FROM books""")
    conn.commit()
    conn.close()

def clear_entry():
    pass

root = Tk()
root.title("Student Book Tracker")
root.geometry("500x400")

srch_label = Label(root, text = "Search:")
srch_label.place(x = 566, y = 0)

srch_entry = Entry(root)
srch_entry.place(x = 620, y = 0)

b_label = Label(root, text = "Borrow Book")
b_label.place(x = 0, y = 0)

fieldset = ttk.Frame(root, borderwidth = 3, relief = "raised")
fieldset.pack(padx = 10, pady = 10, fill = "y", side = "left")

sn_label = Label(fieldset, text = "Student Name:")
sn_label.grid(row = 1, column = 0)

sn_entry = Entry(fieldset)
sn_entry.grid(row = 1, column = 1)

bk_label = Label(fieldset, text = "Book:")
bk_label.grid(row = 2, column = "0", sticky = "w")

bk_entry = ttk.Combobox(fieldset)
bk_entry.grid(row = 2, column = 1) 

bd_label = Label(fieldset, text = "Borrow Date:")
bd_label.grid(row = 3, column = 0, sticky = "w")

bd_entry = DateEntry(fieldset, date_pattern = "dd/mm/yyyy")
bd_entry.grid(row = 3, column = 1)

rtd_label = Label(fieldset, text = "Return Date:")
rtd_label.grid(row = 4, column = 0, sticky = "w")

rtd_entry = DateEntry(fieldset, date_pattern = "dd/mm/yyyy")
rtd_entry.grid(row = 4, column = 1)

add = Button(fieldset, text = "Add", bg = "green", fg = "white", command = add_to_borrowed)
add.grid(row = 5, column = 0)

delete = Button(fieldset, text = "Delete", bg = "red", fg = "white", command = del_from_db)
delete.grid(row = 5, column = 1, padx = 50)

clear = Button(fieldset, text = "Clear", bg = "grey", fg = "black", command = clear_entry)
clear.grid(row = 5, column = "2")

def books_table():
    conn = sqlite3.connect("library.db")

    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                book TEXT NOT NULL, 
                quantity INTEGER NOT NULL)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS borrowed_books (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                student_name TEXT NOT NULL, 
                book_id INTEGER,
                
                borrow_date TEXT CHECK (borrow_date LIKE '%/%/%'), 
                return_date TEXT CHECK (return_date LIKE '%/%/%'), 
                fine REAL DEFAULT 0.00,

                CONSTRAINT FK_books FOREIGN KEY (book_id) REFERENCES books(id))""")
                
    #cur.execute(f"""INSERT INTO books (id, book, quantity) VALUES (1,"{book}", 5)""")

    
    #conn.commit()
    #conn.close()

books_table()

def View():
    con1 = sqlite3.connect("library.db")
    cur1 = con1.cursor()
    cur1.execute("SELECT * FROM books")
    rows = cur1.fetchall()    
    for row in rows:
        print(row) 
        tree.insert("", END, values=row)        
    con1.close()

tree = ttk.Treeview(root, column=("c1", "c2", "c3"), show='headings')
tree.column("#1", anchor=CENTER)
tree.heading("#1", text="id")
tree.column("#2", anchor=CENTER)
tree.heading("#2", text="book")
tree.column("#3", anchor=CENTER)
tree.heading("#3", text="quantity")
tree.pack(side = "right")
button1 = Button(text="Display data", command=View)
button1.pack(pady=10)

root.mainloop()