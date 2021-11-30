DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	email TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL
);

INSERT INTO users (first_name, last_name, email, password) VALUES ("UserFirstName", "UserLastName", "email@email.com", "cucubau");