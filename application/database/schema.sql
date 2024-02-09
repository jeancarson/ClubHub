CREATE TABLE login (
    userID INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

--CREATE TABLE users (
--    userID INTEGER NOT NULL,
--    user_type TEXT NOT NULL,
--    first_name TEXT,
--    last_name TEXT,
--    age INTEGER,
--    email TEXT,
--    phone TEXT,
--    gender TEXT
--);
