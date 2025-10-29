from tkinter import * 
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3

root = Tk()
root.title("Student Book Tracker")
root.geometry("500x400")
root.configure(bg = "lightgrey")

srch_frame = Frame(root, bg = "lightgrey")

srch_label = Label(root, text = "Search:")
srch_label.place(x = 566, y = 0)

srch_entry = Entry(root)
srch_entry.place(x = 620, y = 0)

b_label = Label(root, text = "Borrow Book")
b_label.place(x = 0, y = 0)

fieldset = ttk.Frame(root, borderwidth = 3, relief = "raised")
fieldset.pack(padx = 10, pady = 10, fill = "y", side = "left")

sn_label = Label(fieldset, text = "Student Name:")
sn_label.grid(row = 1, column = 0, pady = (0, 10))

sn_entry = Entry(fieldset, width = 23)
sn_entry.grid(row = 1, column = 1, pady = (0, 10))

bk_label = Label(fieldset, text = "Book:")
bk_label.grid(row = 3, column = "0", sticky = "w", pady = (0, 10))

bk_entry = ttk.Combobox(fieldset)
bk_entry.grid(row = 3, column = 1, pady = (0, 5))

bd_label = Label(fieldset, text = "Borrow Date:")
bd_label.grid(row = 5, column = 0, sticky = "w", pady = (0, 10))

bd_entry = DateEntry(fieldset, date_pattern = "dd/mm/yyyy", width = 15, pady = (0, 5))
bd_entry.grid(row = 5, column = 1)

rtd_label = Label(fieldset, text = "Return Date:")
rtd_label.grid(row = 7, column = 0, sticky = "w")

rtd_entry = DateEntry(fieldset, date_pattern = "dd/mm/yyyy", width = 15)
rtd_entry.grid(row = 7, column = 1)

add = Button(fieldset, text = "Add", bg = "green", fg = "white")
add.grid(row = 9, column = 0)

delete = Button(fieldset, text = "Delete", bg = "red", fg = "white")
delete.grid(row = 9, column = 1, padx = 50)

clear = Button(fieldset, text = "Clear", bg = "grey", fg = "black")
clear.grid(row = 9, column = "2")

def view():
    con1 = sqlite3.connect("library.db")
    cur1 = con1.cursor()
    cur1.execute("SELECT * FROM borrowed_books")
    rows = cur1.fetchall()    
    for row in rows:
        print(row) 
        tree.insert("", END, values=row)        
    con1.close()

tree = ttk.Treeview(root, column = ("c1", "c2", "c3", "c4", "c5", "c6"), show = "headings")
tree.column("#1", anchor = CENTER)
tree.heading("#1", text = "ID")
tree.column("#2", anchor = CENTER)
tree.heading("#2", text = "Student")
tree.column("#3", anchor = CENTER)
tree.heading("#3", text = "Book")
tree.column("#4", anchor = CENTER)
tree.heading("#4", text = "Borrow Date")
tree.column("#5", anchor = CENTER)
tree.heading("#5", text = "Return Date")
tree.column("#6", anchor = CENTER)
tree.heading("#6", text = "Fine")
tree.pack(side = "right")


view()

root.mainloop()