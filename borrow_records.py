from database import execute, fetchone, fetchall

def borrow_book(user_id, book_id):
    query = "CALL borrow_book(%s, %s)"
    params = (user_id, book_id)
    execute(query, params)
    return {"message": "Book borrowed successfully"}

def return_book(book_id):
    query = "CALL return_book(%s)"
    params = (book_id,)
    execute(query, params)
    return {"message": "Book returned successfully"}

def get_borrow_records():
    query = "SELECT * FROM borrow_records"
    return fetchall(query)

def get_borrow_record(record_id):
    query = "SELECT * FROM borrow_records WHERE id = %s"
    params = (record_id,)
    return fetchone(query, params)
