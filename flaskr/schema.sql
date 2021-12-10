DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	user_type TEXT NOT NULL,
	email TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL
);

INSERT INTO users (first_name, last_name, email, password) VALUES ("UserFirstName", "UserLastName","Admin", "email@email.com", "cucubau");
INSERT INTO users (first_name, last_name, email, password) VALUES ("Adi", "Stefan","User", "adi@email.com", "pass123");
