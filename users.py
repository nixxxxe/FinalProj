from database import fetchone, fetchall

def validate_user_credentials(email, password):
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    params = (email, password)
    user = fetchone(query, params)
    return user

def create_user(name, age, department, email, password):
  username = email
  query = "CALL create_user(%s, %s, %s, %s, %s, %s)"
  params = (name, age, department, email, username, password)
  result = fetchone(query, params)
  return result["id"]

def get_users():
  query = "SELECT * FROM get_users"
  result = fetchall(query)
  return result

def get_user(id):
  query = "SELECT * FROM get_users WHERE id = %s"
  params = (id,)
  result = fetchone(query, params)
  return result

def update_user(id, name, age, department, email, password):
  username = email
  query = "CALL update_user(%s, %s, %s, %s, %s, %s, %s)"
  params = (id, name, age, department, email, username, password)
  result = fetchone(query, params)
  return result["id"]

def delete_user(id):
  query = "CALL delete_user(%s)"
  params = (id,)
  result = fetchone(query, params)
  return result["id"]