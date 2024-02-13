CREATE TABLE users (
    user_id     INTEGER     NOT NULL PRIMARY KEY,
    username    TEXT        NOT NULL UNIQUE,
    password    TEXT        NOT NULL,
    approved    INTEGER     NOT NULL CHECK (approved in (0, 1)),
    first_name  TEXT,
    last_name   TEXT,
    age         INTEGER,
    email       TEXT,
    phone       TEXT,
    gender      TEXT
);

CREATE TABLE students (
    user_id     INTEGER     PRIMARY KEY,
    FOREIGN KEY (user_id)   REFERENCES users (user_id)
);

CREATE TABLE coordinators (
    user_id     INTEGER     PRIMARY KEY,
    FOREIGN KEY (user_id)   REFERENCES users (user_id)
);

CREATE TABLE administrators (
    user_id     INTEGER     PRIMARY KEY,
    FOREIGN KEY (user_id)   REFERENCES users (user_id)
);
