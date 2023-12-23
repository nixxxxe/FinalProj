from database import fetchone, fetchall, execute

def add_book(title, author, isbn):
    query = "INSERT INTO books (title, author, isbn) VALUES (%s, %s, %s)"
    params = (title, author, isbn)
    execute(query, params)
    return fetchone("SELECT LAST_INSERT_ID() AS id")['id']

def update_book(book_id, title, author, isbn):
    query = "UPDATE books SET title = %s, author = %s, isbn = %s WHERE id = %s"
    params = (title, author, isbn, book_id)
    execute(query, params)
    return book_id

def delete_book(book_id):
    query = "DELETE FROM books WHERE id = %s"
    params = (book_id,)
    execute(query, params)
    

def get_books():
    query = "SELECT * FROM books"
    return fetchall(query)

def get_book(book_id):
    query = "SELECT * FROM books WHERE id = %s"
    params = (book_id,)
    return fetchone(query, params)

def borrow_book(user_id, book_id):
    query = "CALL borrow_book(%s, %s)"
    params = (user_id, book_id)
    execute(query, params)
    # You might fetch some data or handle any additional actions after borrowing
    # For instance, you could fetch the borrowed book's details if needed
    return get_borrowed_book_details(book_id)

def get_borrowed_book_details(book_id):
    query = "SELECT * FROM books WHERE id = %s"
    params = (book_id,)
    return fetchone(query, params)
