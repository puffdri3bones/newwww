import sqlite3

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
                
    cur.execute(f"INSERT INTO books (id, book, quantity) VALUES (1,'Spiderman', 10)")
    cur.execute(f"INSERT INTO books (id, book, quantity) VALUES (2,'Ironman', 6)")
    cur.execute(f"INSERT INTO books (id, book, quantity) VALUES (3,'The Hulk', 12)")
    cur.execute(f"INSERT INTO books (id, book, quantity) VALUES (4,'Superman', 8)")
    cur.execute(f"INSERT INTO books (id, book, quantity) VALUES (5,'Batman', 3)")
    
    cur.execute(f"INSERT INTO borrowed_books (id, student_name, book_id, borrow_date, return_date, fine) VALUES (1, 'Peter Parker', 'Spiderman', 06/10/25, 06/20/25, 12)")
    
    conn.commit()
    conn.close()

books_table()