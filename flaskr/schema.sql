DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	email TEXT NOT NULL UNIQUE,
	password TEXT NOT NULL,
	is_admin INTEGER DEFAULT 0
);

INSERT INTO users (first_name, last_name, email, password, is_admin) VALUES ("UserFirstName", "UserLastName", "email@email.com", "cucubau", 1);

DROP TABLE IF EXISTS token;
CREATE TABLE token (
	user_id INTEGER,
	token TEXT NOT NULL,
	gen_date TEXT NOT NULL,
	last_access TEXT NOT NULL
);