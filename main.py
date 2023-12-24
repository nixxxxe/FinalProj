from flask import Flask, jsonify, redirect, request
from flask_mysqldb import MySQL
from users import create_user, get_users, get_user, update_user, delete_user
from database import set_mysql
import books
from books import borrow_book 
from books import get_book, update_book
from borrow_records import get_borrow_records
from flask import render_template
from flask import redirect
from database import execute, fetchone, fetchall
app = Flask(__name__, template_folder='templates')
import borrow_records
from flask import url_for
import datetime




# Required
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_PORT"] = 3306
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "HDR*110302res"
app.config["MYSQL_DB"] = "dblibrarymanagement"
# Extra configs, optional but mandatory for this project:
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["MYSQL_AUTOCOMMIT"] = True


mysql = MySQL(app)
#to call set the mysql and pass mysql in the database.py, like a connector
set_mysql(mysql)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/users", methods=["GET", "POST"])
def users():
  if request.method == "POST":
    data = request.get_json()
    user_id = create_user(
      data["name"], data["age"], data["department"],
      data["email"], data["password"]
    )
    return jsonify({"id": user_id})
  else:
     users = get_users()
     return render_template("users.html", users=users)
    
@app.route("/users/<int:id>", methods=["GET", "PUT", "DELETE"])
def user(id):
  if request.method == "PUT":
    data = request.get_json()
    user_id = update_user(
      id,
      data["name"], data["age"], data["department"],
      data["email"], data["password"]
    )
    return jsonify({"id": user_id})
  elif request.method == "DELETE":
    user_id = delete_user(id)
    return jsonify({"id": user_id})
  else:
    user = get_user(id)
    return jsonify(user)
  
@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()
    book_id = books.add_book(data["title"], data["author"], data["isbn"])
    return jsonify({"id": book_id})

@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book_handler(book_id):
    data = request.get_json()
    updated_id = books.update_book(book_id, data["title"], data["author"], data["isbn"])
    return jsonify({"id": updated_id})

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_boook(book_id):
    deleted_id = books.delete_boook(book_id)
    return jsonify({"id": deleted_id})

@app.route("/books", methods=["GET"])
def list_books():
    all_books = books.get_books()
    return render_template("books.html", books=all_books)

@app.route("/books/<int:book_id>", methods=["GET"])
def get_specific_book(book_id):
    book = books.get_book(book_id)
    if book:
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"})
    
def update_user_is_borrowing(user_id, is_borrowing):
    query = "UPDATE users SET is_borrowing = %s WHERE id = %s"
    params = (is_borrowing, user_id)
    execute(query, params)
    
@app.route("/borrow", methods=["POST"])
def borrow():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    book_id = data.get("book_id")
    user_id = data.get("user_id")

    if not book_id or not user_id:
        return jsonify({"error": "Book ID and User ID are required."}), 400

    # Check if the book is available
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT available FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()

    if not book:
        cursor.close()
        return jsonify({"error": "Book not found."}), 404

    if book["available"] == 0:
        cursor.close()
        return jsonify({"error": "Book is already borrowed."}), 400

    # Update the book's availability to indicate it's borrowed
    cursor.execute("UPDATE books SET available = 0 WHERE id = %s", (book_id,))

    # Record the borrowing transaction in the borrow_records table
    current_time = datetime.datetime.now()
    cursor.execute(
        "INSERT INTO borrow_records (user_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, NULL)",
        (user_id, book_id, current_time),
    )

    cursor.close()
    return jsonify({"message": "Book borrowed successfully."}), 200


@app.route("/return/<int:book_id>", methods=["POST"])
def return_book(book_id):
    result = borrow_records.return_book(book_id)

    # Get the user ID associated with the returned book (you may need to fetch it from your database)
    user_id = get_user_id_from_book(book_id)

    # Update the user's is_borrowing status to FALSE
    update_user_is_borrowing(user_id, False)

    return jsonify(result)


def get_user_id_from_book(book_id):
    # Write a SQL query to fetch the user ID associated with the book (based on borrow records)
    query = "SELECT user_id FROM borrow_records WHERE book_id = %s AND return_date IS NULL"
    params = (book_id,)
    result = fetchone(query, params)

    if result:
        return result["user_id"]
    else:
        # Handle the case where the book is not currently borrowed
        return None


@app.route("/borrow_records", methods=["GET"])
def view_borrow_records():
    records = borrow_records.get_borrow_records()
    return jsonify(records)

@app.route("/borrow_records/<int:record_id>", methods=["GET"])
def view_borrow_record(record_id):
    record = borrow_records.get_borrow_record(record_id)
    if record:
        return jsonify(record)
    else:
        return jsonify({"error": "Borrow record not found"}), 404
    
@app.route("/add-book", methods=["GET"])
def add_book_page():
    return render_template("addBook.html")

@app.route("/books/<int:book_id>/edit", methods=["GET"])
def edit_book_page(book_id):
    book = get_book(book_id)  # Fetch book details based on the book_id
    return render_template("editBook.html", book=book)  # Pass book details to pre-fill the form

@app.route("/books/<int:book_id>/update", methods=["POST"])
def update_book_route(book_id):
    # Get the updated book details from the form
    updated_title = request.form.get("title")
    updated_author = request.form.get("author")
    updated_isbn = request.form.get("isbn")

    # Update the book details in the database
    updated_id = update_book(book_id, updated_title, updated_author, updated_isbn)
    
    # Redirect to the book details page after updating
    return redirect(f"/books")


@app.route("/books/<int:book_id>/delete", methods=["POST"])
def delete_book_route(book_id):
    # Perform deletion of the book from the database using the book_id
    books.delete_book(book_id)

    # Redirect to the page displaying the list of books after deletion
    return redirect("/books")

@app.route("/borrow-book")
def borrow_page():
    # You might fetch borrow records data here if needed
    # Fetch borrow records data (assuming you have a function to retrieve it)
    borrow_records = get_borrow_records()  # This fetches the data from your database
    # Then render the borrow_records.html template
    return render_template("borrowRecords.html")

def fetch_available_books():
    # Write a SQL query to fetch the available books from your database
    query = "SELECT * FROM books WHERE available = 1"  # Assuming "1" represents available books

    # Execute the query and fetch the results
    available_books = fetchall(query)

    return available_books


@app.route("/available_books", methods=["GET"])
def get_available_books():
    # Fetch the list of available books from your database
    available_books_list = fetch_available_books()  # Use a different variable name here
    # Return the list of available books as JSON
    return jsonify(available_books_list)

@app.route('/return-book', methods=['GET', 'POST'])
def return_book_form():
    if request.method == 'POST':
        # Get the form data
        book_id = int(request.form.get('book_id'))
        user_id = int(request.form.get('user_id'))

        # Find the book in your database using the get_book function
        book_to_return = get_book(book_id)

        if book_to_return:
            # Check if the book is currently borrowed
            if is_book_borrowed(book_id):
                # Perform the book return actions here
                # For example, you might want to record the return date in your borrow_records table
                record_book_return(book_id, user_id)

                # Redirect to a confirmation page or back to the list of books
                return redirect(url_for('book_list'))  # Replace 'book_list' with your book list route name
            else:
                # Book is already available
                return render_template('return_book.html', error='Book is already available.')
        else:
            # Book not found
            return render_template('return_book.html', error='Book not found.')

    # If it's a GET request, render the return book form
    return render_template('return_book.html', error=None)  # Create a 'return_book.html' template for the form

def is_book_borrowed(book_id):
    # Write a SQL query or implement a function to check if the book is currently borrowed
    # You can use the borrow_records table to check if there's an active borrowing record for the book
    query = "SELECT * FROM borrow_records WHERE book_id = %s AND return_date IS NULL"
    params = (book_id,)
    result = fetchone(query, params)

    return result is not None

def record_book_return(book_id, user_id):
    # Write a SQL query or implement a function to record the book return
    # You should update the borrow_records table to set the return_date for the corresponding record
    current_time = datetime.datetime.now()
    query = "UPDATE borrow_records SET return_date = %s WHERE book_id = %s AND user_id = %s AND return_date IS NULL"
    params = (current_time, book_id, user_id)
    execute(query, params)


# @app.route("/return/<int:book_id>", methods=["POST"])
# def return_book(book_id):
#    result = return_book(book_id)
#    return jsonify(result)

# @app.route("/borrow_records/<int:record_id>/delete", methods=["POST"])
# def delete_borrow_record(record_id):
#    deleted_id = delete_borrow_record(record_id)
#    return jsonify({"id": deleted_id})

