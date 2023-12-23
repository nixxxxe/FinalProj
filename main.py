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

app = Flask(__name__, template_folder='templates')
import borrow_records




# Required
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL-PORT"] = 3306
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "MD_avila.21"
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
    
@app.route("/borrow", methods=["POST"])
def borrow():
    data = request.get_json()
    result = borrow_records.borrow_book(data["user_id"], data["book_id"])
    return jsonify(result)

@app.route("/return/<int:book_id>", methods=["POST"])
def return_book(book_id):
    result = borrow_records.return_book(book_id)
    return jsonify(result)

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

# @app.route("/return/<int:book_id>", methods=["POST"])
# def return_book(book_id):
#    result = return_book(book_id)
#    return jsonify(result)

# @app.route("/borrow_records/<int:record_id>/delete", methods=["POST"])
# def delete_borrow_record(record_id):
#    deleted_id = delete_borrow_record(record_id)
#    return jsonify({"id": deleted_id})

