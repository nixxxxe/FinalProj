CREATE TABLE `students` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `age` int NOT NULL,
  `department` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB 

CREATE TABLE `users` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `username` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB 

CREATE VIEW get_users AS
SELECT
  s.name,
  s.age,
  s.department,
  s.email,
  u.id,
  u.username,
  u.password
FROM students s
INNER JOIN users u ON u.student_id = s.id;

DELIMITER $$
CREATE PROCEDURE create_user(
  IN s_name varchar(200),
  IN s_age int,
  IN s_department varchar(200),
  IN s_email varchar(200),
  IN s_username varchar(200),
  IN s_password varchar(200)
)
BEGIN
  DECLARE v_student_id int;
  INSERT INTO students(name, age, department, email) VALUES(s_name, s_age, s_department, s_email);
  SET v_student_id = LAST_INSERT_ID();
  INSERT INTO users(student_id, username, password) VALUES(v_student_id, s_username, s_password);
  SELECT LAST_INSERT_ID() AS id;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE update_user(
  IN user_id int,
  IN s_name varchar(200),
  IN s_age int,
  IN s_department varchar(200),
  IN s_email varchar(200),
  IN s_username varchar(200),
  IN s_password varchar(200)
)
BEGIN
  UPDATE students
  INNER JOIN users ON users.student_id = students.id
  SET name = s_name, age = s_age, department = s_department, email = s_email
  WHERE users.id = user_id;
  UPDATE users SET username = s_username, password = s_password
  WHERE id = user_id;
  SELECT user_id AS id;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE delete_user(IN user_id int)
BEGIN
  DELETE FROM students WHERE id = (SELECT student_id FROM users WHERE id = user_id);
  DELETE FROM users WHERE id = user_id;
  SELECT user_id AS id;
END$$
DELIMITER ;

CREATE TABLE `books` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `isbn` varchar(20) NOT NULL,
  `available` boolean NOT NULL DEFAULT TRUE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE `borrow_records` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `book_id` int NOT NULL,
  `borrow_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `return_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`user_id`) REFERENCES users(`id`),
  FOREIGN KEY (`book_id`) REFERENCES books(`id`)
) ENGINE=InnoDB;


DELIMITER $$
CREATE PROCEDURE borrow_book(IN user_id int, IN book_id int)
BEGIN
  IF (SELECT available FROM books WHERE id = book_id) THEN
    UPDATE books SET available = FALSE WHERE id = book_id;
    INSERT INTO borrow_records(user_id, book_id) VALUES(user_id, book_id);
  END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE return_book(IN book_id int)
BEGIN
  UPDATE books SET available = TRUE WHERE id = book_id;
  UPDATE borrow_records SET return_date = NOW() WHERE book_id = book_id AND return_date IS NULL;
END$$
DELIMITER ;
