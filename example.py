from tkinter import ttk
from tkinter import *
import sqlite3
"""def connect():
    con1 = sqlite3.connect("example.db")
    cur1 = con1.cursor()
    cur1.execute("CREATE TABLE IF NOT EXISTS table1(id INTEGER PRIMARY KEY, First TEXT, Surname TEXT)")
    con1.commit()
    con1.close()"""
def View():
    con1 = sqlite3.connect("library.db")
    cur1 = con1.cursor()
    cur1.execute("SELECT * FROM books")
    rows = cur1.fetchall()    
    for row in rows:
        print(row) 
        tree.insert("", END, values=row)        
    con1.close()
# connect to the database
#connect() 
root = Tk()
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



