import sqlite3

def books_table():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()

    # Create books table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            book TEXT NOT NULL, 
            quantity INTEGER NOT NULL
        )
    """)

    # Create borrowed_books table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS borrowed_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            student_name TEXT NOT NULL, 
            book_id INTEGER,
            borrow_date TEXT, 
            return_date TEXT, 
            fine REAL DEFAULT 0.00,
            CONSTRAINT FK_books FOREIGN KEY (book_id) REFERENCES books(id)
        )
    """)

    # Insert sample books
    cur.executemany("""
        INSERT INTO books (book, quantity) VALUES (?, ?)
    """, [
        ('Spiderman', 10),
        ('Ironman', 6),
        ('The Hulk', 12),
        ('Superman', 8),
        ('Batman', 3)
    ])

    # Insert a few borrowed book records
    cur.executemany("""
        INSERT INTO borrowed_books 
        (student_name, book_id, borrow_date, return_date, fine)
        VALUES (?, ?, ?, ?, ?)
    """, [
        ('Peter Parker', 1, '06/10/25', '06/10/25', 0),
        ('Bruce Banner', 3, '06/10/25', '06/10/25', 0),
        ('Clark Kent', 4, '06/10/25', '06/10/25', 0)
    ])

    conn.commit()
    conn.close()

books_table()
