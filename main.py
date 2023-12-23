from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from users import create_user, get_users, get_user, update_user, delete_user
from database import set_mysql
import books
from books import borrow_book 
from flask import render_template

app = Flask(__name__, template_folder='templates')
import borrow_records


# Required
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL-PORT"] = 3306
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
def update_book(book_id):
    data = request.get_json()
    updated_id = books.update_book(book_id, data["title"], data["author"], data["isbn"])
    return jsonify({"id": updated_id})

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    deleted_id = books.delete_book(book_id)
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


#@app.route("/borrow", methods=["POST"])
#def borrow_book_route():
#   data = request.get_json()
#    user_id = data.get("user_id")
#    book_id = data.get("book_id")

    # Call the borrow_book function from books.py with user_id and book_id
#    borrowed_book = borrow_book(user_id, book_id)

    # Return the borrowed book's details in the response
#    return jsonify({"message": "Book borrowed successfully!", "book_details": borrowed_book})
    
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